# Security Notes & Manual Steps (must read before deployment)

1) **Create Council SSH Keys** - distribute private keys only to named council members (Alfred, Sara, Bioarchitettura, Dietmar).
2) **Create LUKS Encrypted Vault on the server** - example:
   ```
   dd if=/dev/zero of=/srv/astrod_kernel/astrod_vault.img bs=1M count=200
   cryptsetup luksFormat /srv/astrod_kernel/astrod_vault.img
   cryptsetup open /srv/astrod_kernel/astrod_vault.img astrod_vault
   mkfs.ext4 /dev/mapper/astrod_vault
   mount /dev/mapper/astrod_vault /mnt/astrod_vault
   ```
3) **Only after the vault is unlocked** copy `astrod/astroddeepaura_healing.py` into /mnt/astrod_vault and run it there (if and only if you trust the environment).
4) **Forgejo setup**: follow official Forgejo docs to install into /srv/forgejo as user 'council'. Configure it to listen on localhost:3000 and let Nginx reverse proxy.
5) **TLS**: Use certbot to obtain certificates for a council-controlled domain, or use self-signed certs if access is strictly via IP and Tor hidden service.
6) **Tor hidden service (optional but recommended)**: configure Tor on the VPS and add a hidden service pointing to 127.0.0.1:443. Keep .onion address private.
7) **Backups**: keep daily encrypted backups offsite to council-controlled storage (Isola Parallelis backup recommended).
8) **Incident response**: If Harmonic Sentinel reports anomalies, immediately disconnect network interfaces and perform forensic snapshot.
