# passwordmgr

I got inspired by Computerphile's video about password managers so I made my own.
It's bad I know, but I had fun doing it!

Any feedback on this mess of code is appreciated!

Backend
================
- Store the users credentials (Done!)
- Store the users vault (Done!)
- Encrypt the users vault (Done!)

Frontend
================
- Derive a key based on user's credentials (PBKDF2)
- Decrypt and Encrypt the users vault
