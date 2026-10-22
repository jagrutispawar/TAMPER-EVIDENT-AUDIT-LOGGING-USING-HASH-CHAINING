# Viva Questions and Answers

**1. What is the title of your project?**  
Tamper-Evident Audit Logging Using Hash Chaining.

**2. What is audit logging?**  
It is the recording of important system events such as logins, file updates, and failed access attempts.

**3. What is the objective of this project?**  
To detect unexpected changes to stored audit records using SHA-256 hashing and hash chaining.

**4. What is a hash?**  
A fixed-length digest generated from input data by a hash function.

**5. Which hash algorithm is used?**  
SHA-256, provided by Python's `hashlib` module.

**6. What is hash chaining?**  
Each record stores the hash of the preceding record, creating a linked sequence.

**7. What is `previous_hash`?**  
It stores the previous record's hash. The first record uses a fixed genesis hash.

**8. What is `entry_hash`?**  
It is the SHA-256 digest calculated from the current record's fields, excluding `entry_hash` itself.

**9. Why is canonical JSON used?**  
To serialize the same data consistently before hashing.

**10. What happens if a record is modified?**  
The recalculated hash differs from the stored hash, so verification fails.

**11. Does the project prevent tampering?**  
It mainly detects tampering. Additional controls are required to prevent or resist attacks.

**12. Is hashing the same as encryption?**  
No. Hashing creates a one-way digest; encryption protects confidentiality and is reversible with the appropriate key.

**13. Why use JSON?**  
It is a simple way to store structured records locally for this educational prototype.

**14. Why use Streamlit?**  
It provides a simple browser-based interface using Python.

**15. What is the genesis hash?**  
A fixed initial hash value used as the previous hash for the first record.

**16. What are the limitations?**  
A person with full access to the local file can rewrite the entire chain. The prototype also lacks authentication and protected remote storage.

**17. How can security be improved?**  
Use access controls, remote append-only storage, digital signatures, independently stored checkpoints, monitoring, and backups.

**18. What are the future enhancements?**  
Authentication, role-based access, database storage, alerts, signed checkpoints, and remote log storage.
