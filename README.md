# Molding manufacturing shop

State dated 2026-10-07. Five source designs are forked and pinned. An original printer, removable-pallet and cooling-buffer specification and FreeCAD generator start the design work. Dimensions are provisional. CAD execution and manufacturing release remain open.

## Contents

1. [My research](#1-my-research)
2. [Discoveries](#2-discoveries)
3. [Design and builds](#3-design-and-builds)
4. [Open questions and decisions](#4-open-questions-and-decisions)
5. [Verification](#5-verification)
6. [Pickup](#6-pickup)

## 1. My research

The owner wants a large printer connected to a molding manufacturing shop, with conveyor/pallet transfer or robot unloading and fresh-plate loading. Downstream work should proceed while the next print runs. GitHub is the shared hub. Grok and this Codex chat are intended collaborators; no external chat message has been sent.

Local PostgreSQL keyword search returned no BigFDM hits. A thermal-expansion search returned Holder, An Introduction to Computational Science, section 11.1, PDF page 396, block holder-an-introduction-to-computational-science:p0395:b0003. That passage does not establish printer dimensions or material coefficients. Current primary sources supply printer evidence.

| Owner fork | Upstream | Pinned commit | Role and terms |
|---|---|---|---|
| [egc365/BigFDM](https://github.com/egc365/BigFDM) | fab-machines/BigFDM | 2c222bdee2b6c6f5e23a807b35774b98fa5a98eb | Large printer CAD; CERN-OHL-W-2.0 |
| [egc365/Voron-2](https://github.com/egc365/Voron-2) | VoronDesign/Voron-2 | a192410e27ea345644ae5c4b29b4c9c40cbe1a73 | Existing printer reference; GPL-3.0 |
| [egc365/RatRig-PrintedParts](https://github.com/egc365/RatRig-PrintedParts) | Rat-Rig/RatRig-PrintedParts | c8a6c0d74f5f79a5fab015c5392d188cf12d3384 | Published parts; preserve upstream terms |
| [egc365/RatRig-Panels](https://github.com/egc365/RatRig-Panels) | Rat-Rig/RatRig-Panels | 94dd0f4768a73e6e6cc9db9f204c6dd04c937f68 | Published panels; preserve upstream terms |
| [egc365/replac3d](https://github.com/egc365/replac3d) | jerryli08/replac3d | d6d2e56e3277d414d7a0578e43404a11cc680a0c | Plate changer reference; no declared license, do not copy implementation |

Exact identities are in [sources.lock.json](sources.lock.json). Forking preserves source history; it does not establish unrestricted reuse rights.

[BigFDM README](https://github.com/fab-machines/BigFDM/blob/2c222bdee2b6c6f5e23a807b35774b98fa5a98eb/README.md) is not paginated; source lines 32-45 list an 800 x 800 x 900 mm printing area. Its CAD tree contains BigFDM.f3d and BigFDM v1.step.zip. The roughly EUR 2600 BOM claim is historical, not a current quote.

[Mosaic Array](https://mosaicmfg.com/products-hardware/array/) describes bed swapping and job storage. [Replac3d](https://www.jerryli.design/projects/build-plate-robot) describes an actual plate-changing robot. [Blackbelt](https://blackbelt-3d.com/the-blackbelt-3d-printer/) is a conveyor-printing reference. Commercial systems remain links, not claimed open CAD.

[Voron official repositories](https://github.com/VoronDesign) did not provide a verified Phoenix CAD release during this research. [Rat Rig V-Core 4.1](https://ratrig.com/products/rat-rig-v-core-4-1) provides assembly viewers and states noncommercial design terms. Rat Rig forks contain published parts and panels, not a verified complete V-Core 4.1 assembly.

## 2. Discoveries

A removable carrier allows predictable handling while retaining Z screws and heater wiring inside the printer. This is the first design hypothesis, not the final owner-approved architecture. The pallet and printed part need continuous support during transfer.

BigFDM reports hot-end heating limitations at a 1 mm nozzle and interrupted USB streaming. [Klipper](https://www.klipper3d.org/Features.html) separates host planning from timed MCU execution and supports synchronized MCUs. A dedicated laptop is a host candidate. Stations still require confirmed state transitions and interlocks.

[Vacuum silicone degassing and pressure resin curing](https://support.smooth-on.com/knowledgebase.php?article=47) are different processes. Vacuum bagging is another tooling route. Material and mold use determine the station. No pressure or vacuum vessel is designed in this layout.

## 3. Design and builds

### CELL-001. Printer, pallet and cooling buffer

[design/cell-spec.json](design/cell-spec.json) records requirements, reference/provisional dimensions, interfaces, cycle and acceptance. [cad/build_cell.py](cad/build_cell.py) is original FreeCAD concept code. It creates frame solids, fixed support placeholder, movable pallet, print envelope and cooling-buffer support. The transfer_travel property models pallet displacement.

When executed, the generator checks solid validity and transfer expression, saves/reopens native CAD, and exports/reimports STEP. These are concept conformance checks, not manufacturing certification. Execution is pending.

The 800 x 800 x 900 mm printing envelope references BigFDM. The 850 x 850 x 10 mm pallet, 1100 x 1100 x 1500 mm frame, 400 mm transfer elevation and 200 mm gap are provisional author choices. They are not measurements of BigFDM's physical bed or load-analysis results. Gantry motion hardware, transfer supports, clear exit opening, clamps, locating pins and heaters remain to be engineered.

- [x] Verify five fork parents and commits.
- [x] Separate source specifications and provisional dimensions.
- [x] Parse generator and verify initial layout fit arithmetic.
- [ ] Execute generator in existing FreeCAD runtime.
- [ ] Verify saved native and STEP geometry and transfer behavior.
- [ ] Import BigFDM on a copy and measure physical interfaces.
- [ ] Size supported transfer for actual pallet and part mass.
- [ ] Measure hot/cold flatness, registration and cycle behavior.
- [ ] Select and verify molding process.
- [ ] Release fabrication drawings and current BOM.

Proposed flow is load pallet, print, park, transfer, cool/inspect, finish/seal if needed, then process-specific molding. A fresh pallet lets the printer restart while downstream work proceeds.

## 4. Open questions and decisions

Target part size/mass, print material, casting material, finish, cure temperature and production rate remain unspecified. Existing 350 mm printer ownership is recorded; exact model remains unverified.

The local project folder under Documents is pending the owner's response. No temporary report tree or unrelated CAD project was created. This README is the single project master and will be updated in place. Local recorder setup and CAD execution follow the established destination.

Public hub and forks follow the request for open research and forked sources. Original project licensing remains open. Preserve upstream notices. Replac3d has no declared repository license; it is a reference and no implementation was copied.

## 5. Verification

Authenticated GitHub readback verified five forks, upstream parents and pinned revisions. The hub is public under egc365. Initial committed file contents are checked by exact remote readback.

Python syntax and pallet width/depth and print-envelope height fit are checked. These do not establish executed CAD, collision safety, load capacity, thermal behavior or hardware performance. CAD and machine receipts remain pending.

No printer or molding process was run. Existing models and services were unchanged. Earlier web investigation was not recorded. Local work recording has not started while the destination is pending.

## 6. Pickup

Continue in this master and repository; do not duplicate reports. Skills used are CAD engineering, research, Poteto Mode, playbook and unslop. Installed CAD instructions are at /home/egc365/Documents/skills/cad-engineering/SKILL.md.

Establish the local folder and project-scoped recorder, clone hub and BigFDM, read local instructions, then import BigFDM STEP on a copy with hash, units, body count and bounds. Run CELL-001 in the existing FreeCAD runtime and retain actual native/STEP receipts. Keep manufacturing release open.

GitHub issues track mechanical import, supported transfer and process requirements. Coordinate Grok changes through owned files or branches when the owner connects its work.
