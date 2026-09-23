# Admitting the agents to a server

The agents reach a server as a user of their own, `kntnt-agent`, with the key `setup` made on this machine, `~/.ssh/kntnt-agent`, and never through root's `authorized_keys`. That user has the same power as root through passwordless `sudo`, and a trail of its own in the auth and sudo logs, and a switch of its own to turn off. On a server this Skill creates and a configuration tool converges, the agents' key sits in root's `authorized_keys` from creation until the tool's converge takes it out, and the agents never use it there.

## What the server holds

- A user `kntnt-agent` with a home directory and a login shell, and no password.
- Its `~/.ssh/authorized_keys`, mode `0600` in a `0700` directory, both owned by that user, holding one line: the options `no-port-forwarding,no-agent-forwarding,no-X11-forwarding`, then the public key `setup` printed. The agents need no tunnel, no forwarded agent and no display, so the key grants none of them.
- A drop-in `/etc/sudoers.d/kntnt-agent`, mode `0440`, holding `kntnt-agent ALL=(ALL) NOPASSWD:ALL`, checked with `visudo -cf` before it is put in place. A drop-in that does not parse can lock every user out of `sudo`.

## Who manages the server

Settle this for a server before the agents are admitted to it or turned off on it. A configuration tool, Ansible for example, manages a server when it converges that server's accounts, SSH keys, sudoers or sshd configuration, and each converge undoes a hand change to what it covers. Settle it from the project at hand, the repository this Skill runs in, and from nothing else: its deployment documentation and its infrastructure files, read as step 1 of *Establish the operation* reads them. Assume no particular tool and no particular layout.

- **A tool manages it.** The files of the project at hand show a configuration tool converging the server. For a server that exists, the tool's inventory, or its equivalent, names the server. For a server this Skill is about to create, the files show the tool converging the group, role or environment the new server joins, and the instruction or the deployment documentation of the project at hand names that group. The agents are admitted as *Admission through a configuration tool* states.
- **Nothing converges it.** The project at hand describes its servers, and no tool covers this server or the group it joins. *The procedure* applies, carried out as *Who carries it out* states.
- **Unsettled.** The project at hand does not describe the servers, or does not say which group a new server joins. This is common, since `/hetzner setup` names a Hetzner project rather than a repository and often runs where nothing describes the servers. Where the Skill would admit the agents or turn them off itself, it asks the user who manages the server before any write, and takes the path the answer settles. For a server this Skill creates, it asks after creation and before admission: creation attaches the agents' key as [provisioning.md](provisioning.md) states and changes nothing a tool owns.

*The procedure* is run only on a server nothing converges, never on one a tool manages or one still unsettled. Where the Skill only shows the steps for a server rather than taking them, it shows the one path this check settles for that server. For a server the check leaves unsettled, it shows both, each opened by the condition it applies under: admission through the tool, for a server a configuration tool manages; *The procedure*, for a server nothing converges.

## Admission through a configuration tool

On a server a configuration tool manages, the agents become an administrator of their own in the mechanism the project at hand declares its administrators with, and a converge puts them on the server. Adding the agents' key to an administrator the project at hand already declares, the operator included, is not admission, and *The procedure* is never run there. A server this Skill creates is created as [provisioning.md](provisioning.md) states, the agents' key attached, and its checks after creation run over root's login.

The account the tool makes meets this contract, all three parts of it:

- everything *What the server holds* lists, for a user `kntnt-agent` with `~/.ssh/kntnt-agent.pub` as its key;
- `kntnt-agent` in `AllowUsers` or `AllowGroups`, where sshd limits logins with either;
- no line of `/root/.ssh/authorized_keys` holding the agents' key.

1. Before any change, find the mechanism the project at hand declares its administrators with, and read it for what the contract asks of the account: no password, the three `no-*-forwarding` options on the key's line, passwordless `sudo` through a drop-in of its own, and a place in `AllowUsers` or `AllowGroups` where sshd limits logins. Where there is no such mechanism, or it cannot express one of these, stop as *Where the project at hand falls short* states.
2. Declare `kntnt-agent`, with `~/.ssh/kntnt-agent.pub` as its key, where the project at hand declares its administrators, and take the change through the workflow of the project at hand: its review, its tests, its merge rule. A converge then puts it on the servers.
3. Carry this as far as the instruction authorizes and the rules of the project at hand let an agent go, and report what is still owed, such as a review, a merge, a converge, or the checks below. Until the converge has run on a server this Skill created, what is owed includes the converge taking the agents' key out of root's `authorized_keys`.
4. After the converge, check from this machine, with the host key checked as [provisioning.md](provisioning.md) states:

   ```sh
   ssh -i ~/.ssh/kntnt-agent -o IdentitiesOnly=yes kntnt-agent@<server> sudo -n true
   ssh -i ~/.ssh/kntnt-agent -o IdentitiesOnly=yes kntnt-agent@<server> sudo -n cat /root/.ssh/authorized_keys
   ```

   The first exits 0 when the agents are admitted. In what the second prints, look for the key field, the second field, of `~/.ssh/kntnt-agent.pub`; a file that does not exist holds no key. Where the key is still there, the tool falls short of the contract: stop as below. These two commands are the whole check on the server.

### Where the project at hand falls short

The project at hand may have no way to declare another administrator, or its mechanism may not express every part of the contract, such as the forwarding options, the drop-in, a place in `AllowUsers`, or taking the agents' key out of root's `authorized_keys`. Say which of the two it is, name the part that is missing, and stop. The fix belongs in the tool of the project at hand: on a server a tool manages, the next converge undoes a hand edit, so neither *The procedure* nor a hand edit completes the missing part, and root's `authorized_keys` is never edited by hand.

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

Each case is for a server nothing converges, as *Who manages the server* settles.

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

Settle who manages the server first, as *Who manages the server* states.

On a server a configuration tool manages, the agents are turned off by removing their declaration through the workflow of the project at hand and converging. Carry it as far as the instruction authorizes and the rules of the project at hand let an agent go, and report what is still owed, as for admission.

On a server nothing converges, removing `/etc/sudoers.d/kntnt-agent` takes the root power away and leaves the login. `usermod --expiredate 1 kntnt-agent` shuts the login as well, and `userdel --remove kntnt-agent` removes the user and its home. The user's own access is untouched by all three.
