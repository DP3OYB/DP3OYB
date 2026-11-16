# Custom firmware changes

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
