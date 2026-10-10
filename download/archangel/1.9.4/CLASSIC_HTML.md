# Classic HTML profile in 1.9.4

The public index.html uses HTML 4.01 structural vocabulary and a conservative
subset of CSS 2-era typography/block layout, available before 2010. References:
https://www.w3.org/TR/html401/ and
https://www.w3.org/TR/2009/CR-CSS2-20090423/ . CSS 2.1 was a candidate in 2009;
its final recommendation came later. This profile is a feature subset, not a
claim of final CSS 2.1 recommendation status in 2010 or universal old-browser support.

Output uses div/span, headings, paragraphs, lists, block quotes, pre/code, links,
tables, and local PNG images. It has no required scripts, external fonts,
service images, HTML5-only semantic elements/attributes, CSS custom properties,
Grid, Flexbox, clamp, viewport units, modern word-breaking, or rounded corners.
Content metadata uses ordinary HTML4 meta elements. The archive retains JSON,
Markdown and integrity companion files; the public webpage is index.html.
Connection requests must be disabled explicitly before selecting this profile.
Classic has a light palette. Retro appearance can also be used with Modern HTML.

UTF-8 text and local PNGs remain portable. Export and preview image paths differ
only so the private preview can show embedded bytes; the public ZIP uses assets/.
Print reading preview does not promise identical pagination across browsers.
