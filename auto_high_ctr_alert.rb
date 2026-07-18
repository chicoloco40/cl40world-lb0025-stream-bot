# ====================== STREAM ALERT COMMANDS ======================

ADMIN_IDS = [1315843947297509396, 1482904022695284808]

def admin?(event)
  ADMIN_IDS.include?(event.user.id) ||
    event.user.roles.any? { |r| r.name.downcase.include?("admin") || r.name.downcase.include?("mod") }
end

# !golive - Admin only
bot.message(with_text: '!golive') do |event|
  next unless admin?(event)

  embed = Discordrb::Webhooks::Embed.new
  embed.title = "🔴 CL40 World is LIVE!"
  embed.description = "Chico Loco 40 & LB0025 are streaming right now!"
  embed.color = 0xFF0000
  embed.timestamp = Time.now

  embed.add_field(name: "📺 YouTube", value: "[Watch Live](https://www.youtube.com/@chicoloco40)", inline: true)
  embed.add_field(name: "📺 YouTube", value: "[Watch Live](https://www.youtube.com/@lb0025-o6s)", inline: true)
  embed.add_field(name: "🎮 KICK", value: "[Watch Live](https://kick.com/chicoloco40live)", inline: true)
  embed.add_field(name: "🐦 X", value: "[Watch Live](https://x.com/chicoloco_off)", inline: true)
  embed.add_field(name: "🎵 Apple Music", value: "[Watch Live](https://music.apple.com/gb/artist/chico-loco-40/1763913299)", inline: true)
  embed.add_field(name: "🎵 Apple Music", value: "[Watch Live](https://music.apple.com/gb/artist/lb0025/1763916955)", inline: true)
  embed.add_field(name: "🎶 TIDAL", value: "[Watch Live](https://tidal.com/artist/49911535/u)", inline: true)
  embed.add_field(name: "🎶 TIDAL", value: "[Watch Live](https://tidal.com/artist/54468017/u)", inline: true)
  embed.add_field(name: "🎵 Spotify", value: "[Watch Live](https://open.spotify.com/artist/22fLaOOBnTXVHiM7fe16jZ?si=Iho0aSiXQgqxSfrPIto-dA)", inline: true)
  embed.add_field(name: "🎵 Spotify", value: "[Watch Live](https://open.spotify.com/artist/73On3dmwuzbJZFbdKuHBsy?si=yOLJNEFkRCGCpdRO2sa2JQ)", inline: true)
    embed.add_field(name: "🎵 Amazon Music", value: "[Watch Live](https://music.amazon.co.uk/artists/B0DDS3JTB5/chico-loco-40)", inline: true)
  embed.add_field(name: "🎵 Amazon Music", value: "[Watch Live](https://music.amazon.co.uk/artists/B0DDSHRJYW/lb0025?marketplaceId=)", inline: true)
  embed.add_field(name: "🎵 Anghami", value: "[Watch Live](https://open.anghami.com/MhNr7nd1S4b)", inline: true)
  embed.add_field(name: "🎵 Anghami", value: "[Watch Live](https://open.anghami.com/Ar3eFKk1S4b)", inline: true)

  

  




  

  embed.add_field(name: "🌍 Official Links", value: 
    "[CL40 World](https://cl40.contact) | [Founder](https://founder.cl40.world) | [Press](https://press.cl40.world)\n" +
    "[Discord Main](https://discord.gg/H5cw3bexg) | [Discord B2C](https://discord.gg/4ucb2Yes)", inline: false)

  embed.footer = Discordrb::Webhooks::EmbedFooter.new(text: "CL40 World • Powered by Grok & xAI • Sovereignty Mode ON")

  event.channel.send_embed("", embed)
end

# !stream - Public
bot.message(with_text: '!stream') do |event|
  event.respond "🔴 **CL40 World LIVE**\n\n" +
                "YouTube: https://youtube.com/@chicoloco40\n" +
                "YouTube: https://youtube.com/@lb0025-o6s\n" +
                "https://music.apple.com/us/artist/chico-loco-40/1763913299" +
                "https://music.apple.com/us/artist/chico-loco-40/1763913299" +
                "https://music.amazon.co.uk/artists/B0DDS3JTB5/chico-loco-40" +
                "https://music.amazon.co.uk/artists/B0DDSHRJYW/lb0025?marketplaceId=" +
                "KICK: https://kick.com/chicoloco40live\n\n" +
                "Official: https://www.patreon.com/CL40world/posts/beats-pack-euro-163601436?utm_medium=clipboard_copy&utm_source=copyLink&utm_campaign=postshare_creator&utm_content=join_link"
                "Official: https://cl40.contact"
end
