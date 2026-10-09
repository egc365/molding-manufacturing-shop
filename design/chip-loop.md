# CHIP-001. Zero-loss metal loop

State 2026-10-08. Constraint from the owner: metal CNC for boring, capture every chip, do not buy a melt cycle, fold a printer into the same cell. Laser-as-particle-source is rejected on energy, not on taste.

## Why the laser path fails the constraint

Ablation pays vaporization, not fusion. Latent heat of vaporization for aluminum is about 10 MJ/kg; fusion is about 0.4 MJ/kg. A laser that turns chips into dust spends more energy than a furnace, then loses mass to fume, oxidation, and filters. That is the opposite of "lose nothing" and "do not heat it for a lot of money."

Tiny screws come off the mill from bar. Dust is not an intermediate. Consolidation of dust still needs pressure plus heat or a binder.

## Loop that matches the constraint

1. Cut. Existing mill. Boring and screw work stay subtractive.
2. Catch. Enclosure, flood or MQL, conveyor, cyclone, sealed bin. Weigh stock in, part out, bin out. Gap is the loss number.
3. Keep solid. Chips stay chips. No melt.
4. Rebuild later, solid-state only. Friction-extrude or friction-stir the chips into bar. Cold briquette is storage, not a screw.
5. Printer stays polymer. CELL-001 prints pallets, ducts, fixtures. It does not print the metal.

## What got forked, and what it is for

Motion, not a compiler:

- egc365/grbl
- egc365/Grbl_Esp32
- egc365/LaserGRBL
- egc365/LaserWeb4
- egc365/All4Laser
- egc365/OLSK-Small-Laser

Printer host, already the shop path:

- egc365/klipper
- egc365/Marlin

Maskless microfab, only if a later station is lithography. Not the metal loop:

- egc365/stepper
- egc365/sclmt

reprap/reprap does not exist (404). reprap/firmware fork was rate-limited. Marlin is the living RepRap firmware.

## Open

Mill controller, envelope, alloy, and whether the bin is weighed in-cell. No BOM until those four are named.
