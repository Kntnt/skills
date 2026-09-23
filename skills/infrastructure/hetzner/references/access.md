# Admitting the agents to a server

The agents reach a server as a user of their own, `kntnt-agent`, with the key `setup` made on this machine, `~/.ssh/kntnt-agent`, and never through root's `authorized_keys`. That user has the same power as root through passwordless `sudo`, and a trail of its own in the auth and sudo logs, and a switch of its own to turn off.

## What the server holds

- A user `kntnt-agent` with a home directory and a login shell, and no password.
- Its `~/.ssh/authorized_keys`, mode `0600` in a `0700` directory, both owned by that user, holding one line: the options `no-port-forwarding,no-agent-forwarding,no-X11-forwarding`, then the public key `setup` printed. The agents need no tunnel, no forwarded agent and no display, so the key grants none of them.
- A drop-in `/etc/sudoers.d/kntnt-agent`, mode `0440`, holding `kntnt-agent ALL=(ALL) NOPASSWD:ALL`, checked with `visudo -cf` before it is put in place. A drop-in that does not parse can lock every user out of `sudo`.

## The procedure

Run as root on the server — through `sudo` where the login in use is not root's — with `KEY` set to the public key `setup` printed. It converges: run again, it leaves the same state.

```sh
KEY='ssh-ed25519 AAAA... kntnt-agent@host'
id kntnt-agent >/dev/null 2>&1 || useradd --create-home --shell /bin/bash kntnt-agent
HOME_DIR=$(getent passwd kntnt-agent | cut -d: -f6)
install -d -m 0700 -o kntnt-agent -g kntnt-agent "$HOME_DIR/.ssh"
printf 'no-port-forwarding,no-agent-forwarding,no-X11-forwarding %s\n' "$KEY" > "$HOME_DIR/.ssh/authorized_keys"
chown kntnt-agent:kntnt-agent "$HOME_DIR/.ssh/authorized_keys"
chmod 0600 "$HOME_DIR/.ssh/authorized_keys"
DROP_IN=$(mktemp)
printf 'kntnt-agent ALL=(ALL) NOPASSWD:ALL\n' > "$DROP_IN"
visudo -cf "$DROP_IN" && install -m 0440 -o root -g root "$DROP_IN" /etc/sudoers.d/kntnt-agent
rm -f "$DROP_IN"
```

Where the server's `sshd_config` limits logins with `AllowUsers` or `AllowGroups`, add `kntnt-agent` there and validate with `sshd -t` before reloading, keeping the current session open as [provisioning.md](provisioning.md) says for any change to SSH access.

Then verify from this machine, with the host key checked as [provisioning.md](provisioning.md) states:

```sh
ssh -i ~/.ssh/kntnt-agent -o IdentitiesOnly=yes kntnt-agent@<server> sudo -n true
```

It exits 0 when the agents are admitted. `sudo -n` fails rather than waits where the drop-in is missing.

## Who carries it out

- **A server this Skill creates** gets the agents' key at creation, which Hetzner installs for root. After its host key is verified and cloud-init has finished, run the procedure over that root login, verify the `kntnt-agent` login as above, then remove the agents' key from `/root/.ssh/authorized_keys`, leaving the user's own key there. From then on the agents reach it as `kntnt-agent` alone.
- **A server that already exists**, where the instruction authorizes admitting the agents and the server is reachable with the user's own key: enable its protection first, as the Execution boundaries require before a first write, then run the procedure over the user's login and verify it.
- **Any other server**: print the procedure with `KEY` filled in, for the user to run as root in the server's console or in a session of their own. This is the one step only the user can take on a server the agents cannot yet reach.

## Reaching a server as the agents

Host operations run as `kntnt-agent` through `sudo`, as root only where the instruction says so:

```sh
ssh -i ~/.ssh/kntnt-agent -o IdentitiesOnly=yes kntnt-agent@<server> sudo -n <command>
```

Never copy, print or move the private key; it stays on this machine.

## Turning it off

Removing `/etc/sudoers.d/kntnt-agent` takes the root power away and leaves the login. `usermod --expiredate 1 kntnt-agent` shuts the login as well, and `userdel --remove kntnt-agent` removes the user and its home. The user's own access is untouched by all three.
