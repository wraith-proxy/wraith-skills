# Crypto-shredding in BigQuery

Erase a subject by deleting their key, not their rows.

- One data key per subject in a keystore table, wrapped by a Cloud KMS key (`KEYS.NEW_KEYSET`, `KEYS.KEYSET_CHAIN`).
- Encrypt classified columns with AEAD. Use deterministic encryption (`DETERMINISTIC_ENCRYPT`) for the subject identifier used in joins and randomized encryption (`AEAD.ENCRYPT`) for other classified columns, binding the subject id as additional authenticated data.
- Encrypted columns are BYTES, so they cannot be partition or cluster keys.
- Join to the keystore with LEFT JOIN, so rows whose key was shredded surface as NULL plaintext.
- Erasure deletes the subject's key row. Time travel (2 to 7 days, set per dataset) and fail-safe (7 days) delay physical erasure; state both in the retention policy.
- Plaintext must not persist upstream. Raw tables holding plaintext personal data need their own retention or encryption, or the shred is incomplete. Backups and exports are copies and need the same treatment.
- Classification comes from the ODCS contract (wraith:odcs-contracts).

## Sketch

Replace `<kms_key_uri>` with the Cloud KMS key from the project's Terraform.

```sql
-- Keystore: two wrapped keysets per subject, keyed by a random surrogate
-- subject_key (never the natural id), so a shredded row identifies nobody.
CREATE TABLE IF NOT EXISTS keystore.subject_keys (
  subject_key STRING NOT NULL,
  det_keyset BYTES NOT NULL,   -- DETERMINISTIC_AEAD_AES_SIV_CMAC_256
  aead_keyset BYTES NOT NULL   -- AEAD_AES_GCM_256
);

INSERT INTO keystore.subject_keys
SELECT
  GENERATE_UUID(),
  KEYS.NEW_WRAPPED_KEYSET('<kms_key_uri>',
    'DETERMINISTIC_AEAD_AES_SIV_CMAC_256'),
  KEYS.NEW_WRAPPED_KEYSET('<kms_key_uri>', 'AEAD_AES_GCM_256')
FROM staging.new_subjects;  -- one row per subject without a key

-- Encrypt: deterministic id for joins, randomized AEAD for the rest,
-- with subject_key bound as additional authenticated data.
SELECT
  p.subject_key,
  DETERMINISTIC_ENCRYPT(
    KEYS.KEYSET_CHAIN('<kms_key_uri>', k.det_keyset),
    p.subject_id, p.subject_key) AS subject_id_enc,
  AEAD.ENCRYPT(
    KEYS.KEYSET_CHAIN('<kms_key_uri>', k.aead_keyset),
    p.email, p.subject_key) AS email_enc
FROM staging.people AS p
JOIN keystore.subject_keys AS k USING (subject_key);

-- Decrypt: LEFT JOIN so shredded subjects return NULL plaintext.
SELECT
  e.subject_key,
  DETERMINISTIC_DECRYPT_STRING(
    KEYS.KEYSET_CHAIN('<kms_key_uri>', k.det_keyset),
    e.subject_id_enc, e.subject_key) AS subject_id,
  AEAD.DECRYPT_STRING(
    KEYS.KEYSET_CHAIN('<kms_key_uri>', k.aead_keyset),
    e.email_enc, e.subject_key) AS email
FROM curated.people AS e
LEFT JOIN keystore.subject_keys AS k USING (subject_key);
```
