# Salon Prize Wheel

A live, on-screen prize wheel for social media giveaways. Open `index.html` in any modern browser (double-click it). No install needed.

## Running the draw
1. **Load names**: click *Upload spreadsheet* (.xlsx / .xls / .csv), pick the column with the names, then *Load these names*. You can also paste names into the box, one per line.
2. **Settings**:
   - *One entry per person* merges repeated names. Untick it if each like, comment and share counts as its own entry.
   - *Take winners off the wheel* stops anyone winning twice.
   - Set the heading, the prize and how long the spin lasts (15, 20 or 30 seconds; never less than 15).
3. **Go live**: share your screen, click *Presentation mode* (and *Full screen* if you like), then click *Spin the wheel* or press the space bar.
4. The winner pops up with the date, time and number of entries. That makes a good screenshot for your announcement post.

The winner is picked with the browser's cryptographic random number generator (`crypto.getRandomValues`), so every slot has exactly the same chance. Names and winners are saved in the browser, so a page refresh won't lose them.
