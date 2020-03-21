# Describe (beets plugin)

The describe plugin will attempt to give you the full picture on a single attribute of your library.

**NOTE: Under heavy development!**


# Usage:

```bash
beet describe genre
```

You can of course add any queries after the name of the field to describe such as:

```bash
beet describe genre albumartist:'Various Artists'
```

# Sample Output

`beet describe bpm albumartist:'Various Artists'`

```text
┌────────────────┬────────────────────────────┐
│ Name           │                      Value │
╞════════════════╪════════════════════════════╡
│ Field name     │                        bpm │
├────────────────┼────────────────────────────┤
│ Field type     │ beets.dbcore.types.Integer │
├────────────────┼────────────────────────────┤
│ Count          │                       1392 │
├────────────────┼────────────────────────────┤
│ Min            │              65.9922409058 │
├────────────────┼────────────────────────────┤
│ Max            │                      185.0 │
├────────────────┼────────────────────────────┤
│ Mean           │         122.99097545119291 │
├────────────────┼────────────────────────────┤
│ Median         │                      122.0 │
├────────────────┼────────────────────────────┤
│ Empty          │                          0 │
├────────────────┼────────────────────────────┤
│ Unique         │                        649 │
├────────────────┼────────────────────────────┤
│ Most frequent  │                  122.0(22) │
├────────────────┼────────────────────────────┤
│ Least frequent │           117.853546143(1) │
└────────────────┴────────────────────────────┘
Distribution(bins=10) histogram
66.0 - 77.9    [ 30]  ████▊
77.9 - 89.8    [ 73]  ███████████▍
89.8 - 101.7   [203]  ███████████████████████████████▊
101.7 - 113.6  [221]  ██████████████████████████████████▌
113.6 - 125.5  [256]  ████████████████████████████████████████
125.5 - 137.4  [208]  ████████████████████████████████▌
137.4 - 149.3  [183]  ████████████████████████████▋
149.3 - 161.2  [ 87]  █████████████▋
161.2 - 173.1  [107]  ████████████████▊
173.1 - 185.0  [ 24]  ███▊
```

`beet describe genre albumartist:'Various Artists'`

```text
┌────────────────┬───────────────────────────┐
│ Name           │                     Value │
╞════════════════╪═══════════════════════════╡
│ Field name     │                     genre │
├────────────────┼───────────────────────────┤
│ Field type     │ beets.dbcore.types.String │
├────────────────┼───────────────────────────┤
│ Count          │                      1392 │
├────────────────┼───────────────────────────┤
│ Empty          │                        19 │
├────────────────┼───────────────────────────┤
│ Unique         │                        91 │
├────────────────┼───────────────────────────┤
│ Most frequent  │               Oldies(202) │
├────────────────┼───────────────────────────┤
│ Least frequent │              Post-Punk(1) │
└────────────────┴───────────────────────────┘
Unique element histogram
Oldies                  [202]  ████████████████████████████████████████
Classic Rock            [139]  ███████████████████████████▌
Soul                    [124]  ████████████████████████▌
Blues                   [120]  ███████████████████████▊
Rock                    [109]  █████████████████████▋
Pop                     [105]  ████████████████████▊
Dance                   [ 86]  █████████████████
New Wave                [ 48]  █████████▌
Reggae                  [ 44]  ████████▊
Heavy Metal             [ 33]  ██████▌
Trance                  [ 24]  ████▊
Blues Rock              [ 20]  ████
Jazz                    [ 20]  ████
                        [ 19]  ███▊
Soundtrack              [ 17]  ███▍
Ska                     [ 16]  ███▏
Synthpop                [ 16]  ███▏
Rap                     [ 15]  ███
Pop Rock                [ 14]  ██▊
Funk                    [ 12]  ██▍
Metal                   [ 12]  ██▍
Alternative Metal       [ 12]  ██▍
Alternative Rock        [ 11]  ██▏
Soft Rock               [ 10]  ██
Hard Rock               [ 10]  ██
Singer-Songwriter       [  9]  █▊
Rockabilly              [  8]  █▋
Metalcore               [  6]  █▎
Electronic              [  6]  █▎
Rock And Roll           [  6]  █▎
R&B                     [  6]  █▎
House                   [  5]  █
Disco                   [  5]  █
Progressive Rock        [  5]  █
Psychedelic Rock        [  5]  █
Punk Rock               [  4]  ▊
Thrash Metal            [  4]  ▊
Progressive Metal       [  4]  ▊
Contemporary R&B        [  3]  ▋
Nu Metal                [  3]  ▋
Symphonic Metal         [  3]  ▋
Funk Soul               [  3]  ▋
World Music             [  3]  ▋
Death Metal             [  3]  ▋
Britpop                 [  2]  ▍
Industrial Metal        [  2]  ▍
PMEDIA                  [  2]  ▍
Contemporary Classical  [  2]  ▍
Post-Grunge             [  2]  ▍
Psychedelic             [  2]  ▍
Motown                  [  2]  ▍
Glam Rock               [  2]  ▍
Rock, Hard Rock, Metal  [  2]  ▍
Blue-Eyed Soul          [  2]  ▍
Black Metal             [  2]  ▍
Indie Rock              [  2]  ▍
Indie Pop               [  2]  ▍
Industrial              [  2]  ▍
Pop Punk                [  2]  ▍
Surf Rock               [  2]  ▍
Hip Hop                 [  1]  ▎
Gospel                  [  1]  ▎
Ragga                   [  1]  ▎
Indie                   [  1]  ▎
Speed Metal             [  1]  ▎
Gypsy Jazz              [  1]  ▎
Gothic Metal            [  1]  ▎
Country                 [  1]  ▎
Viking Metal            [  1]  ▎
Melodic Metalcore       [  1]  ▎
Southern Soul           [  1]  ▎
Sludge Metal            [  1]  ▎
Country Rock            [  1]  ▎
Pop Soul                [  1]  ▎
Industrial Rock         [  1]  ▎
Grunge                  [  1]  ▎
Southern Rock           [  1]  ▎
Ballad                  [  1]  ▎
Teen Pop                [  1]  ▎
Dance-Pop               [  1]  ▎
Lo-Fi                   [  1]  ▎
Power Metal             [  1]  ▎
Vocal Trance            [  1]  ▎
Folk Rock               [  1]  ▎
Downtempo               [  1]  ▎
Doo Wop                 [  1]  ▎
Blackgaze               [  1]  ▎
Pinoy Rock              [  1]  ▎
Classical               [  1]  ▎
Grindcore               [  1]  ▎
Post-Punk               [  1]  ▎
```

