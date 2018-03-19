# Changelog
Detailed changes for commits.
## Unreleased
- Redistribute plots for better readability.
- Auto highlights of data (award system).
- Hours of the day with more activity.
- Mentions of participants.
- Read files with 12 hour format.
- Complete support for `es` and `fr`.
## 0.0.3 - 2018-03-19
### Added
- Natural Language Processing plots:
  - Most used words.
  - Most used emoji.
- Language auto detection (only supports `en` and `es`).
- Save figure as `png` with `-s` argument (figure is save in the same directory as the chat file loaded).
### Fixed
- Overlapping for anonymized names in +12 members groups.
- Unordered labels when using anonymized option.
### Known bugs
- Stacked emojis interpreted as one new unknown emoji.
- Labels for emoji not displayed properly.
## 0.0.2 - 2018-03-18
### Added
- General group data.
- [Hidden] Spam coefficient (relationship between messages sent and words).
- Mean values.
- Anonymized names using `-a` after `path` argument
### Removed
- Senders' legend (was redundant and difficult to fit).
### Fixed
- Improved font size scaling for +8 members groups.
## 0.0.1 - 2018-03-17
### Added
- CHANGELOG file.
- Parser for WhatsApp file format (iOS and Android).
- Initial analysis of number of messages, senders and number of words.
- Plots: Total messages, proportion text/media, words per message and total words.
