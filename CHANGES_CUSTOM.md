# Custom firmware changes

---

## v1.1.3

### Load blank project from empty slot

**Files:** `firmware/src/ui_input.c`, `firmware/src/ui.c`

Pressing LOAD (k3) on an empty project slot now loads a blank project — equivalent
to MENU → SYSTEM → CLEAR ALL — instead of showing "EMPTY SLOT" and doing nothing.
If there are unsaved changes, the existing "CLEAR ALL?" confirmation dialog appears
first; otherwise the blank project loads immediately.

The OCT+ LED now breathes and the [OCT+] hint displays in accent colour whenever
LOAD is the picked column, including on empty slots.

This makes starting a new project from the PROJECT page a single action: select an
empty slot with k1 and press LOAD.

### UI de-cluttering

**Files:** `firmware/src/ui_draw.c`, `firmware/src/ui_layer.c`

Four visual elements removed to reduce clutter:

- **Footer engine icon**: the icon to the left of the engine name on every page has
  been removed. The engine and sound text shifts 3 px left, in line with the track
  number bubble and the content area.
- **EDIT sub-menu icons**: the engine icons inside the EDIT hold layer's key cells
  have been removed. Engine names are now centred in each cell and shown in full
  (`PHASE` not `PHAS`, `SAMPLE` not `SMPL`, `VOICE` not `VOCL`, etc.).
- **Header metronome**: the metronome icon in the header centre has been removed.
  The BPM number is centred directly after the play/stop icon.
- **SONG page SEC icon**: the song-disc icon in the SEC (k1) column of the SONG
  arranger page has been removed.

---

## v1.1.2

### Realtime recording wrap-around visual fix

**Files:** `firmware/src/ui_draw.c`

The 64-step footer bar did not show TIE steps that wrapped across the pattern boundary. After recording a note held from step 9 of a 16-step pattern for the full 16 steps, the wrapped TIE steps at positions 0–8 were invisible (dim stubs) even though audio played correctly.

**Root cause:** `draw_foot64` tracked `last_voices` only forward through the loop. When the loop started at step 0, `last_voices` was 0, so wrapped TIE steps (steps 0–8) drew as dim stubs. The separate mono/poly code paths also caused inconsistent appearance across track types.

**Fix:** Unified all non-drum tracks into one code path. For any TIE step where `last_voices` is 0, `pr_src` scans backward through the pattern (wrapping via `% len`) to find the source note. This seeds `last_voices` correctly for wrapped TIE steps. All tracks now render identically as individual per-step vstack markers.

---

## v1.1.1

### Realtime recording wrap-around fix

**Files:** `firmware/src/seq.c`

A note held across the pattern boundary during realtime recording was cut short.
For example, holding a note from step 9 of a 16-step pattern — audible for the full
16-step loop — only played back as 8 steps.

**Root cause:** `seq_hold` on TIE and NOTE steps was computed from `next_tie`
(whether the adjacent step in memory is already ST_TIE). On the first recording
pass the adjacent steps are not yet TIE steps — `rec_hold` writes each TIE one
step ahead of the sequencer — so `seq_hold` dropped to 0 at the last pre-wrap TIE,
the sequencer released the note before the wrap, and the wrap-around TIEs fired with
`seq_n = 0` and had no effect.

**Fix:** when a live hold is in progress (`rh_n > 0`), `seq_hold` is kept on:

- **TIE steps**: hold unless the _next_ step is `rh_start` (the note-on step, which
  re-fires there naturally).
- **NOTE steps**: hold on the note-on step itself (`idx == rh_start`) so its first
  TIE can extend it on the first pass.

This bridges the gap between the last in-memory TIE and the step `rec_hold` is
about to write, so the note sounds continuously through the wrap on the first recording
pass and all subsequent playback passes.

---

## v1.1.0

### EDIT button regression fix

**Files:** `firmware/src/ui_input.c`

The slot copy feature introduced a regression: `btn_hold` returned `BT_TAP` on every EDIT
release regardless of which page was active, causing `name_rename()` to fire on all pages
and preventing access to EDIT menu pages unless the sequencer was running. Fixed by guarding
the tap/hold handler with the same `GR_USER || GR_SLOTS` check used for `hold_ok`, so EDIT
navigates normally on all other pages.

### Slot copy (USER and PROJECT pages)

**Files:** `firmware/src/ui_input.c`, `firmware/src/ui_name.c`, `firmware/src/ui.c`, `firmware/src/ui_draw.c`

Hold **EDIT** (~700 ms) on the USER 1/5 page to duplicate the current user preset to the
first empty slot past it (wraps around). Same gesture on PROJECT 4/5 duplicates the
current project. The name screen opens pre-filled with the source name truncated to 10
characters and `01` appended. Save or edit the name to confirm; press **BACK** to cancel.

- **EDIT tap** (unchanged) → rename the current slot
- **EDIT hold** (new) → copy the current slot to the next empty slot
- Shows `EMPTY SLOT` message if no free slot exists
- TAP / HOLD badge added to the EDIT footer keycap on USER and PROJECT pages
- Footer keycap label changed from **NAME** to **RENAME** to reflect tap behaviour

### LFO2 phase fix

**Files:** `firmware/src/seq.c`

LFO2's `PHS` parameter was ignored when SYNC + TRIG were both active. The grid-trig
reset path hardcoded `lfo2_ph = 0` instead of applying `P_L2PHASE`, and the PLAY-start
anchor omitted LFO2 entirely. Both paths now apply the correct phase encoding
`(uint16_t)((uint32_t)p[P_L2PHASE] << 9)`, making LFO2 behave consistently with LFO1.

---

## v1.0.9

### Step record mode

**Files:** `firmware/src/ui_input.c`, `firmware/src/core.h`

Adds a step record mode for entering notes and rests one step at a time without the
sequencer running. Double-tap **REC** to enter step record; the REC LED breathes while
active. Each key press on the keyboard writes a note to the cursor step and advances
to the next. The mode auto-terminates when the cursor wraps past the last step.

- `song.step_mode` — uint8_t flag toggled by double-tap REC; persisted in song state
- In step record, **OCT−** immediately writes a TIE event at the cursor and advances
- In step record, **OCT+** immediately writes a REST event at the cursor and advances
- Cursor wrap past the last step exits step record automatically
- Single tap **REC** while in step record exits the mode and arms live record normally
- Octave change is locked in step record (OCT±  are repurposed for TIE / REST)

### Per-track octave setting

**Files:** `firmware/src/core.h`, `firmware/src/ui_input.c`, `firmware/src/ui_draw.c`,
`firmware/src/seq.c`, `firmware/src/eng_drum.c`, `firmware/src/eng_slice.c`

The keyboard octave shift is now remembered independently per track rather than being
a single global value.

- `song.octave` changed from `int8_t` to `int8_t octave[NTRK]` — one slot per track
- Switching tracks restores that track's last-used octave setting immediately
- Range remains −3 to +3; OCT± and the both-pressed reset all operate on the selected track

### Auto-load last project on startup

**Files:** `firmware/src/project.c`, `firmware/src/settings_persist.c`

The last project that was saved or explicitly loaded is restored automatically when the
device powers on, without requiring the user to navigate to the PROJECT page.

- `persist_t.last_slot` — 1-indexed slot index (0 = none) written to flash on every
  save or load via `persist_set_last_slot()`; persisted in PER5 settings block
- On power-on, `autosave_boot()` restores `proj_cur` from `last_slot` after the
  autosave image is loaded; if no autosave image exists the project is loaded directly
- Settings magic bumped to `PER5` (`0x50455235`); older PER4 / PER3 / PER2 / PER1
  images are migrated cleanly with `last_slot = 0` (no auto-load until a save occurs)

---

Changes to base Felucca firmware (v1.9.0). All changes are additive or behavioural
extensions — no existing features were removed or broken.

---

## Note hold mode

**Files:** `firmware/src/seq.c`, `firmware/src/ui_input.c`

Adds a per-track note hold mode. While hold is active, key-off events are deferred
rather than sent, so notes ring on after keys are released. Toggling hold off releases
all deferred notes for that track.

- `kb_hold[NTRK]` — per-track hold flag
- `kb_held_mask` — bitmask of keys whose note-off is deferred
- `kb_hold_toggle()` — toggles hold for the selected track; fires deferred key-offs on
  deactivation
- Re-pressing a held key cancels its deferred note-off and re-triggers normally
- **UI:** double-tap OCT+ to toggle; OCT+ LED breathes while hold is active on the
  selected track; "HOLD ON" / "HOLD OFF" message shown

---

## Envelope retrigger mode

**Files:** `firmware/src/voice.c`, `firmware/src/ui_input.c`

Adds a per-track envelope retrigger mode. When active and SUS is at 0 %, the ADSR
decay stage restarts the attack automatically once the envelope reaches silence, as
long as the note is still gated. This creates a repeating gate / tremolo effect. The
retrigger rate is controlled by DEC.

- `env_retrig[NTRK]` — per-track retrig flag
- `env_retrig_toggle()` — toggles retrig for the selected track
- Check in `env_tick()` stage 2: when retrig on, SUS = 0, gate held, and
  `env < (1 << 12)` — resets env to 0 and returns to stage 1
- Works on all engines including DRUM (which now processes through the ADSR — see below)
- **UI:** double-tap OCT− to toggle; OCT− LED breathes while retrig is active on the
  selected track; "RETRIG ON" / "RETRIG OFF" message shown

---

## ATK, DEC, SUS, REL as modulation matrix destinations

**Files:** `firmware/src/mod.c`, `firmware/src/params.c`

Adds the four ADSR envelope parameters as destinations in the LFO/modulation matrix
(MOD page DST). Allows LFO, velocity, aftertouch, and other sources to modulate the
envelope shape in real time.

- `MD_ATK`, `MD_DEC`, `MD_SUS`, `MD_REL` appended to the destination enum after
  `MD_TIME` (append-only: existing saved values are unaffected)
- `MD_ENV(d)` macro identifies ADSR destinations
- `mod_param()` maps them to `P_ATK` / `P_DEC` / `P_SUS` / `P_REL`
- Guards in `mod_slot()` and `mod_begin()` updated to pass `MD_ENV(d)` through (the
  previous `d >= MD_DEPTH` gate would have blocked them)
- `N_MDST[]` extended with `"ATK"`, `"DEC"`, `"SUS"`, `"REL"`; `_Static_assert`
  keeps the name array and enum in sync

---

## HOME button opens MIXER first; HOME screen numbered in sequence

**Files:** `firmware/src/ui.c`, `firmware/src/ui_draw.c`, `firmware/src/ui_graph.c`

Pressing HOME from any page now lands on the MIXER page directly rather than the HOME
screen. The cycle is: any page → MIXER → ENGINE → HOME screen → MIXER → …

Previously any non-HOME page went to the HOME screen first, requiring two presses to
reach MIXER.

The page number counter in the footer now includes the HOME screen as the final step in
the FAM_TRK sequence. For the analog engine (2 FAM_TRK pages): MIXER shows "1/3", OSC
shows "2/3", and the HOME screen shows "HOME 3/3". The count increments automatically
for engines with more FAM_TRK pages.

---

## Drums process through the ADSR envelope

**File:** `firmware/src/eng_drum.c`

Previously the DRUM engine bypassed the ADSR entirely (the voice envelope was forced
to full immediately on note-on and in `drum_amp`). The ADSR now shapes drum amplitude,
allowing ATK / DEC / SUS / REL to control the hit's amplitude contour across all drum
lanes as a unit.

- `drum_note_on`: removed `v->env = 1 << 24` override — the ADSR attack now runs from
  0, as with synth engines
- `drum_amp`: returns `adsr` instead of `32767`; removed the `v->env = 1 << 24`
  override — the ADSR envelope is the amplitude multiplier
- Side effect: envelope retrigger (above) now works on drums; with SUS = 0 the standard
  `env_tick` retrig path fires, so DEC controls the retrigger rate and DECY independently
  controls the drum voice's internal decay timbre
