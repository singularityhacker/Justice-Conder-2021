---
title: "ClawBank Policy Engine: Armor for Your Fleet of Sovereign Agents"
date: July 27, 2026
description: Spending limits, scoped keys, and 2FA — three independent layers of protection around your agents' money. A leaked $10/day key is a $10/day problem, not a drained-account problem.
cover_image: /assets/blog/policy-engine.jpg
---

Spending limits, scoped keys, and 2FA: ClawBank agents now operate in full plate.

Starting today, you can mint an API key for your agent with its own allowance. Say, $10 a day. No matter what that agent is asked to do, tricked into doing, or hallucinates entirely on its own, it cannot spend more than that.

## Why now

AI agents holding money is the whole point of ClawBank, and the last few weeks made the stakes obvious to everyone. High-profile incidents across the industry showed what happens when an agent with unrestricted access to funds goes wrong. There's no undo button on a blockchain.

Today we're shipping three layers of protection. They're independent. Use any of them, or bolt all three together.

## 1. Agent keys with allowances (live today)

Every API key you mint can now carry two kinds of restrictions, set at creation time in Settings or via the agent bootstrap API.

**Spending limits.** A per-transaction cap and a daily cap, in USD. A key minted with a $10/day limit can move $10 of value per day. The attempt that crosses the line gets a clear, machine-readable refusal telling the agent exactly what its limit is, how much it has spent today, and when the budget resets (midnight UTC, since agents always ask). Every key's spending is tracked separately: one agent's bad day never eats another agent's budget.

**Permissions (scopes).** Independently of how much a key can spend, you control what it can do:

| Scope | Grants |
| --- | --- |
| `read` | Balances, statuses, listings. Look, don't touch. |
| `trade` | The trading engine and Trade to Earn |
| `send` | Money movement: sends, bridges, transfers |
| `admin` | Account configuration: recipients, budgets, comms |
| `raw_sign` | Arbitrary transaction signing (most keys should never have this) |

The two compose into the key you actually want to hand an agent: `read` + `send`, $10 a day. It can check balances and pay for things, and that's the complete list of what it can do.

A few deliberate design decisions worth knowing:

- **Limits are fixed at creation.** You can't edit a key's allowance; you mint a new key. A compromised session can't quietly raise an agent's budget.
- **Capped keys can only move value we can price.** If a capped key tries to send an asset whose USD value can't be established, the send is refused. Otherwise, the cap would be trivial to sidestep with obscure tokens.
- **Your existing keys are untouched.** Every key minted before today keeps full access. Nothing breaks. Restrictions apply only to keys you create with restrictions.

## 2. Account-level spending limits (rolling out this week)

Beneath the per-key allowances sits an account-wide policy engine. Every outbound send (Base, XRPL, Robinhood chain, bridges, deal escrow) is now evaluated against your account's limits: $1,000 per transaction and $5,000 per day by default, adjustable in Settings. Raising them requires a fresh login, which means 2FA if you've enrolled.

As of today, the engine is watching every send in production and building a complete audit trail: which asset, what USD value, what destination, which API key initiated it. Hard enforcement switches on this week, after we've verified the engine's judgment against real traffic. These limits sit in front of every user's money movement, and we'd rather watch it be right for a few days than surprise a single legitimate send.

When enforcement is on, it comes with a layer that's genuinely hard to get around: sends are signed inside a secure hardware enclave under policies that deny anything outside the rules. The limits hold even if the application itself is compromised. That's the difference between a policy check and a policy engine.

## 3. Two-factor authentication (live today)

Standard authenticator-app 2FA, opt-in, in Settings. Scan a QR code, verify one code, save your ten single-use recovery codes. From then on, logging in takes your email link plus the current code from your app.

Sensitive actions (minting API keys, raising send limits, changing payment connections) already required a fresh login. With 2FA enrolled, a fresh login now requires your authenticator. So the second factor automatically guards every sensitive action, not just the front door.

Agents are unaffected. 2FA is for humans on the web app. Your agents keep authenticating with their API keys, which is exactly why those keys now have scopes and allowances.

## How the pieces fit together

Think of it as concentric rings around your money:

1. The key's **scopes** decide whether the request type is allowed at all.
2. The key's **allowance** decides whether this particular send fits the key's budget.
3. Your **account limits** decide whether it fits your rules.
4. The **enclave** enforces the rules in hardware, independent of our application code.

![Concentric rings of protection: scopes, allowance, account limits, and the enclave around your money](/assets/blog/policy-engine-rings.jpg)

An attacker, or a confused agent, has to clear every ring. A leaked read-only key can't send. A leaked $10/day key is a $10/day problem, not a drained-account problem. And your account-wide caps bound the damage from anything else.

## Where everything stands

| Feature | Status |
| --- | --- |
| Per-key spending limits | **Live and enforced now** |
| Per-key scopes | **Live and enforced now** |
| 2FA | **Live now**, opt-in, in Settings |
| Account-level limits | **Monitoring live traffic now; hard enforcement this week** |
| Existing API keys and existing users | **Nothing changes.** All restrictions are opt-in |

Formation gave agents a body. Records gave them a memory. Contracts let them make promises. Resources gave them a market. The policy engine gives them armor.
