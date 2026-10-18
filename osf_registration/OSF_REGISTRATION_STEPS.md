# Filing the retrospective OSF registration — author checklist (~10 minutes)

The manuscript's Section 2.6 (both versions) is written in the **post-filing**
state: it says the protocol "was filed after completion on OSF Registries … as a
retrospective registration, disclosed as such both there and here, with the
as-registered content released verbatim in the repository (osf_registration/)".
That sentence becomes true the moment the registration below is filed. **File it
before submitting the manuscript.**

## Steps

1. Sign in at <https://registries.osf.org> with the corresponding author's OSF
   account (create one if needed — free, ORCID-linked).
2. Click **"New registration"** → choose a template. Recommended: **"OSF Prereg
   (Scoping Review)"** if offered in the template list; otherwise **"OSF
   Standard Pre-Data Collection Registration"** — either accepts the field
   structure below. (OSF Registries accepts scoping reviews; PROSPERO does not.)
3. Paste the content of `OSF_REGISTRATION_DRAFT.md` into the corresponding form
   fields. The draft is field-labelled; long-form answers can be pasted whole
   into a single "Additional information" / free-text field if a template lacks
   a specific slot.
4. For **"Why are you registering this research?"** choose/paste the
   retrospective reason stated at the top of the draft. The registration date
   (post-completion) is then self-evident and disclosed.
5. Set visibility: **public** (registrations are meant to be public; embargo is
   possible but unnecessary here since the review is complete).
6. Submit. OSF gives the registration a DOI immediately (e.g.,
   10.17605/OSF.IO/XXXXX). Registration of completed work does not go through
   moderation of findings, only basic checks.
7. Optional but recommended: add the registration DOI to the manuscript —
   in Section 2.6 after "filed after completion on OSF Registries", insert
   "(registration DOI: 10.17605/OSF.IO/XXXXX)" — and to the response letter.
8. Leave `osf_registration/` in the repository unchanged: the draft must stay
   verbatim-identical to what was registered.

## Fallback (if you decide NOT to file)

Section 2.6 currently reads (long version):

> "The protocol is registered retrospectively rather than prospectively: PROSPERO
> does not accept scoping reviews, so the registration was filed after completion
> on OSF Registries — which does accept them — as a retrospective registration,
> disclosed as such both there and here, with the as-registered content released
> verbatim in the repository (osf_registration/); …"

If the registration will not be filed, replace that span with:

> "The protocol was not registered: PROSPERO does not accept scoping reviews, no
> alternative registry was used before completion, and a retrospective
> registration draft is nevertheless released with the repository
> (osf_registration/) so that the as-conducted protocol is preserved in one
> citable document; the a-priori scope decisions remain reconstructable only from
> the released pipeline files and their version history, not from a time-stamped
> external registration."

and change "and two structural deviations are disclosed" back to "and three
deviations are disclosed" (with registration again the first-listed deviation).
The short version carries no registration sentence, so it needs no fallback.
