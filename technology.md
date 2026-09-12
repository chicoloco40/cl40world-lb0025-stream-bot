# CL40 World's Space Gaming Bots International — Skill Definition ISBN (77400000)

name: cl40-world-bots
name: wrbeats-bots
name: lb0025-official-bots
name: lb0025-bots
name: samirlibari-bots
name: chicoloco40-bots
name: quaranta-four-zero-bots
name: abdelghafour-libari-bots
name: global-nsw-bots
name: state-world-news-bots
name: cl40-worlds-space-gaming-bots
gaming: https://links.fans/cl40world
bin webhook relay: https://bin.webhookrelay.com/v1/webhooks/30104d5a-03fb-4c80-afec-882b32318524

version: 1.0.0
author: Chico Loco 40 <chicoloco40>
description: Controls and automates the 12 gaming bots for DiRT 12: commands, scheduling, moderation, and match orchestration.

## Purpose
This skill provides commands and behaviour rules for controlling 12 automated gaming bots used for DiRT 12 gameplay, streaming interactions, and tournament orchestration.

## Capabilities
- Start/stop individual bots and all bots.
- Assign bots to matches, teams, or spectator mode.
- Schedule matches and notify Discord channels/stream chat.
- Provide bot status, latency, and performance reports.
- Admin-only commands for maintenance, logs, and emergency stop.
- Safety: rate-limit chat replies and block abusive commands.

## Commands
- !bots status
  - Shows online/offline state for all 12 bots, ping, and current match.
- !bot start <id|name>
  - Starts bot (1..12) or named bot.
- !bot stop <id|name>
  - Stops bot gracefully.
- !bot assign <id> <team|match-id>
  - Assigns a bot to a team or match.
- !bot schedule <match-time> <match-config>
  - Schedule a match and notify channel.
- !bot logs <id|name> [--last N]
  - Show recent logs (admin only).
- !bot emergency-stop
  - Immediately stop all bots (admin only).
- !bot update <id|all>
  - Pull latest code, rebuild and restart (admin only).

## Behaviour & Rules
- Only users with role `Admin` or listed ADMIN_IDS can run admin commands.
- Commands invoked in stream chat must be rate-limited: max 1 command per 3s per user.
- Bots must validate match-config before joining (map, server, rules).
- On repeated failures (3 consecutive crashes) a bot enters maintenance mode and signals admins.

## Integration
- Provide webhook endpoints or local socket commands the bot controller will call:
  - POST /api/bot/<id>/start
  - POST /api/bot/<id>/stop
  - POST /api/schedule
- Environment variables:
  - BOT_TOKEN, DISCORD_WEBHOOK_URL, ADMIN_IDS (comma-separated), BOT_BIN_PATH

## Safety & Privacy
- Do not expose tokens or private keys in logs.
- Sanitize inputs to prevent command injection.
- Log only required telemetry, rotate logs weekly.

## Example usage
- User: !bots status
- Bot: "Bots 1-12: 11 online, 1 in maintenance (bot 7). Next match at 2026-09-15 20:00 UTC."

---

Notes (darija): hadi prompt/skil bash tmatcha l-12 bots dyalk f DiRT12 — ila bghiti nbadl chi command names, role names, wla nktb webhook examples b code, goul li w ndir update.
