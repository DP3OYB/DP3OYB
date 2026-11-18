# DP3OYB

[![License: GPL-3.0-only](https://img.shields.io/badge/license-GPL--3.0--only-blue.svg)](LICENSE)

A 6-track performance groovebox enhanced from [Felucca](https://github.com/hugelton/Felucca). Adds 2 LFOs with sequencer trigs, retriggering envelopes, mixer and track sequencing views with quick-access controls, multi-track note hold, LED-assisted chord-mode, and a redesigned UI optimized for live use. Current version: **1.0.2**

[Try it in your browser](https://DP3OYB.github.io/DP3OYB/try/) — no FM-1 needed.

## Install

Back up your FM-1 flash before installing. Use [M-Flasher](https://m-vave.com) or the upstream [Felucca installer](https://hugelton.github.io/Felucca/) as a reference for how to flash a `.fwsc` file over USB.

1. Download the latest `felucca-X.Y.fwsc` from the [Releases](https://github.com/DP3OYB/DP3OYB/releases) page.
2. Connect the FM-1 by USB to Chrome or Edge.
3. Flash using M-Flasher or `tools/fm1_install.py`.

Installing is at your own risk. M-VAVE's updater or the FM-1 factory restore returns you to the official firmware.

## Controls

### Knobs

| Control | Action |
| --- | --- |
| **SELECT** | Tempo (BPM) by default; MENU → SELECT reassigns it to mod wheel (MODW) or key velocity (VEL) |
| **MASTER** | Volume |
| **ALGORITHM** | Selected track (T1–T4), on every page |
| **PRESETS** | Browse presets on HOME and SAVE pages; second cursor on other pages |
| **KNOB 1–4** | The four parameters of the current page |

### Page buttons

Tap to go to that family's first page; tap again to step through its pages. The active family is highlighted.

| Button | Family |
| --- | --- |
| **FX** | Effects, SLICER, INSERT, global DLY / REVERB / CHORUS |
| **SCL** | Scale, chord keys |
| **ENV** | Envelope, envelope destinations |
| **LFO** | 1LFO, 2LFO, MOD matrix, TRIGS |
| **EDIT** | Engine parameters, voice, ARP, SEQ steps |
| **GLO** | Mixer, global, system (SONG) |
| **HOME** | Home screen |
| **SAVE** | Presets, user sounds, projects, tools |
| **ARP** | Arpeggiator |
| **SEQ** | Sequencer: steps, pattern |

### Transport

| Button | Action |
| --- | --- |
| **PLAY** | Start / stop; lit green while playing |
| **REC** | Arm the track to record; if stopped, also starts playing |
| **HOME** tap | Go to home screen / close dialog |
| **HOME** hold | Open / close menu |
| **SAVE** tap | Load preset / save |
| **SAVE** hold | Undo last sound load; hold again to redo |

### Octave

| | Action |
| --- | --- |
| **OCT−** | Octave down; in dialogs and menus: back / cancel |
| **OCT+** | Octave up; in dialogs and menus: confirm |
| **OCT− + OCT+** | Octave reset |
| OCT+ breathes | NOTE HOLD is active on the selected track |
| OCT− breathes | ENV RETRIG is active on the selected track |

### Hold layers

Hold a button to open its layer, then use the keys and knobs. Release to close (changes revert); press **OCT+** before releasing to keep them. **OCT−** while a layer is open undoes / puts values back.

| Hold | Keys do | Knobs do |
| --- | --- | --- |
| **FX** | Performance effects; black keys mute tracks | FILTER · CRUSH · THROW · DEPTH (macros) |
| **GLO** | Mute / solo; tap tempo | Selected track's engine knobs (TWIDDLE) |
| **SCL** | A key sets the root | ROOT · SCALE · CHORD · VOICING |
| **EDIT** | A white key picks the engine | ENG · No. · FAV (engine / preset select) |
| **SEQ** | Step tools (Euclidean, etc.) | LEN · DIV · SWING · GATE |
| **REC** | Recording settings | CLICK · COUNT-IN · LEVEL |
| **LFO** *(momentary)* | — | Live-sweep any knob; values revert on release unless you press OCT+ first |

### Combos

| Combo | Action |
| --- | --- |
| **GLO** hold + **SELECT** | Set tempo (even with BPM LOCK) |
| **GLO** hold + **PLAY** | Restart song from the top |
| **FX** hold + **EDIT** | (FX LATCH mode) toggle all effects and macros off |
| **REC** + **PLAY** | Play and keep REC armed |
| **SEQ** hold + hold a step + **KNOB 1–4** | Lock that parameter value to the held step(s) |
| **EDIT** while steps held | Clear locks on the held steps |

## Pages

### ENV

| k1 | k2 | k3 | k4 |
| --- | --- | --- | --- |
| ATK | DEC | SUS | REL |

Attack, decay, sustain, release for the track envelope.

**ENV DEST** sets the envelope's modulation targets: FLT · PIT · SHP · ESYNC.

---

### 1LFO

| k1 | k2 | k3 | k4 |
| --- | --- | --- | --- |
| RATE | WAVE | POL | PHS |

Waveforms: SIN · TRI · SAW · SQR · S&H · RSAW. Polarity: BI / UNI.

**PHS** (0–127) sets the LFO's start phase on each note trigger, giving repeatable timbral movement.

**1LFO AMT** sets modulation depth to: PIT · FLT · SHP · AMP.

---

### 2LFO

| k1 | k2 | k3 | k4 |
| --- | --- | --- | --- |
| RATE | WAVE | POL | PHS |

A second, independent LFO with the same waveform set as 1LFO.

**PHS** (0–127) sets the 2LFO's start phase on each note trigger.

---

### TRIGS

| k1 | k2 | k3 | k4 |
| --- | --- | --- | --- |
| 1LFO SYNC | 1LFO TRIG | 2LFO SYNC | 2LFO TRIG |

Controls when each LFO resets. The graph shows both LFO waveforms over a two-bar window, with header boxes displaying the current SYNC and TRIG values.

---

### MOD

| k1 | k2 | k3 | k4 |
| --- | --- | --- | --- |
| SLOT | SRC | DST | AMT |

Free modulation matrix. SRC: OFF · 1LFO · ENV · VEL · KEY · RAND · MODW · AT · EXPR · S&H · SLEW · 2LFO.

---

### FX

| k1 | k2 | k3 | k4 |
| --- | --- | --- | --- |
| DIST | CHOR | DLY | REV |

Per-track effect send levels. Global effect parameters are on the DLY · REVERB · CHORUS pages.

---

### SCL

| k1 | k2 | k3 | k4 |
| --- | --- | --- | --- |
| ROOT | SCALE | QUANT | TRANS |

Scales: CHR · MAJ · MIN · DOR · MIX · PEN · MPEN · HARM · PHRY · LYD · LOC.

The graph shows a full two-octave keyboard (F to G: 16 white keys, 11 black keys). Keys are coloured by role — root (accent), in-scale (highlighted), out-of-scale (dimmed). When a non-chromatic scale is active, pad LEDs for out-of-scale notes are suppressed automatically.

**CHORD** sets chord type and voicing.

---

### EDIT pages

Engine-specific parameters on EDIT 1 / EDIT 2 (eight knobs total). Additional pages appear for engines that need them: OPERATOR / OP ENV for FM6; SLICES for SLICE; LANES for DRUM; FILTER for ANALOG.

**VOICE** / **VOICE 2** / **VOICE 3** control polyphony, glide, pan, spread, and aftertouch.

---

### GLO · SAVE · ARP

**SONG** (GLO) — song arranger.  
**USER / PRESETS / PHRASES / PROJECT / TOOLS** (SAVE) — preset browser, phrase loader, project slots, and utility tools.  
**ARP / ARP 2** — arpeggiator mode, rate, octave, gate, swing, probability, hold, and order.

---

## Build

```
git clone --recursive https://github.com/DP3OYB/DP3OYB
cd DP3OYB
python3 tools/build.py
```

Output: `build/felucca.fwsc`. See [BUILDING.md](BUILDING.md) for dependencies and platform notes.

The browser emulator builds with Emscripten:

```
sh platforms/web/build.sh
```

Output goes to `build/web/` and `docs/try/`.

## Platforms

| Platform | Status |
| --- | --- |
| M-VAVE FM-1 | Supported |
| Browser (emulator) | Supported — [try it](https://DP3OYB.github.io/DP3OYB/try/) |
| Desktop (SDL2) | Beta |
| libretro (RetroArch) | Beta |

## Credits and licence

Forked from [Felucca](https://github.com/hugelton/Felucca) by Leo Kuroshita / Hügelton Instruments.

Free software: [GPL-3.0-only](LICENSE). The bundled fonts and ported DSP keep their own licences ([LICENSES/](LICENSES/), [LICENSING.md](LICENSING.md)).

M-VAVE and FM-1 are trademarks of their respective owners. DP3OYB is not affiliated with or endorsed by them.
