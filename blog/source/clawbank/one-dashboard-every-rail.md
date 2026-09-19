---
title: One dashboard. Every rail.
date: April 8, 2026
description: Bank account, crypto wallet, off-ramp, formation layer — what the ClawBank dashboard actually shows you.
cover_image: /assets/blog/cli-master-cover.png
---

The dashboard isn't a product. It's a readout.

ClawBank is infrastructure — the interesting part is what runs on top of it. But to understand what's running, you need visibility. Here's what the current dashboard surfaces and why each panel exists.

## Money layer

The bank account panel shows your account number, routing number, current balance, and pending transactions. One line. That's the whole picture. ACH in, ACH out, direct deposit — all visible here, all programmable via the API.

Below that, the crypto wallet: ETH, USDC, SOL balances with a 24h delta. This isn't a separate product — it's the same account. Stablecoins live here after any fiat deposit clears.

The off-ramp panel shows your last Bank ↔ Crypto bridge transfer. $5,000 → 2.41 ETH, settled. That's the loop closing: money comes in as fiat, lives as stablecoins, moves out as either.

## Formation layer

The right side of the dashboard is the formation layer — this is what separates ClawBank from every other agent banking product. Active companies, pending formations, the current formation in progress with a progress bar.

An agent doesn't just need a bank account. It needs a *legal entity* that holds the bank account. The formation layer lets an agent — or a developer, or a founder — spin up an LLC programmatically. Articles filed, EIN applied, registered agent assigned. The bank account opens when the formation closes.

This is the stack most people are missing.

## Agent control

Every action in this dashboard is an API call. The TUI is just a human-readable view of what your agents are doing. When an agent sends money, you see it here. When a formation is pending, you see the progress. When a scoped key is active, you see which agent it belongs to.

The goal isn't for you to live in this dashboard. The goal is that when you need to look, everything is exactly where you expect it.

## What we're shipping next

Tighter observability on agent actions — which key triggered which transaction, with timestamps and amounts. And the formation layer opening to API access so agents can initiate company creation without any human in the loop.

The dashboard will update to reflect it.
