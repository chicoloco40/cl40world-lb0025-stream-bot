# DSP Release Checklist for CL40 World

## Release Metadata
- [ ] Release title
- [ ] Artist name: Chico Loco 40
- [ ] Label name: CL40 WORLD LLC SYNDICATE PORTAL INTERNATIONAL
- [ ] Tracklist and duration
- [ ] Release type (Single / EP / Album)
- [ ] Release date and time
- [ ] Pre-save / pre-order URLs
- [ ] UPC / Catalog number
- [ ] ISRC codes for each track
- [ ] Genre and mood tags
- [ ] Explicit / clean status
- [ ] Distributor: UnitedMasters
- [ ] Territory / worldwide release settings

## Artwork
- [ ] Cover art image `assets/cover.jpg` or `assets/cover.png`
- [ ] Minimum 3000x3000 pixels
- [ ] JPG or PNG, RGB color profile
- [ ] No text or logo too close to edges

## Digital Platform Targets
- [ ] Spotify
- [ ] Apple Music
- [ ] Tidal
- [ ] Amazon Music
- [ ] YouTube Music
- [ ] Deezer
- [ ] Shazam
- [ ] Anghami

## UnitedMasters Notes
- [ ] Login to UnitedMasters account
- [ ] Upload audio files and artwork
- [ ] Enter artist / label information
- [ ] Map track metadata and ISRCs
- [ ] Set release date and schedule
- [ ] Review and confirm distribution territories
- [ ] Add pre-save / pre-order links if available
- [ ] Add Spotify artist link after submission
- [ ] Confirm email notifications for approval

## Spotify Integration Notes
- [ ] Add `SPOTIFY_CLIENT_ID` to `.env`
- [ ] Add `SPOTIFY_CLIENT_SECRET` to `.env` (keep secret)
- [ ] Create OAuth redirect server for `https://...` redirect URI
- [ ] Exchange authorization code for access/refresh token
- [ ] Store refresh token safely in `settings.json`

## Release Announcement
- [ ] Draft announcement embed message
- [ ] Choose Discord channel to post announcement
- [ ] Add streaming links in announcement
- [ ] Add call-to-action: listen, pre-save, follow

## Deployment
- [ ] Run `python3 bot.py` with `.env` configured
- [ ] Keep `settings.json` and `.env` out of public repos
- [ ] Use a process manager or Docker for 24/7 uptime
- [ ] Monitor logs in `bot.log`
