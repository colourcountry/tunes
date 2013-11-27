\version "2.16.0"

\layout { 
  indent = 0.0\cm
  \context { \Score \remove "Bar_number_engraver" }	
  \context { \Staff \remove "Time_signature_engraver" }
}

#(set-global-staff-size 16)

\paper {

scoreTitleMarkup = \markup {
  \fill-line {
    \line {
      \fontsize #4 \bold  
      \fromproperty #'header:piece
      \normalsize  
      \fromproperty #'header:subtitle
      \normal-text
      (\fromproperty #'header:opus)
    }
    \line {
      \italic
      \fromproperty #'header:meter
    }
  }
}

}

ossia = \with {
      \remove "Time_signature_engraver"
      alignAboveContext = #"main"
      fontSize = #-3
      \override StaffSymbol #'staff-space = #(magstep -3)
      \override StaffSymbol #'thickness = #(magstep -3)
      firstClef = ##f
}

makePercent =
#(define-music-function (parser location note) (ly:music?)
   "Make a percent repeat the same length as NOTE."
   (make-music 'PercentEvent
               'length (ly:music-length note)))

makeDoublePercent =
#(define-music-function (parser location note) (ly:music?)
   "Make a percent repeat the same length as NOTE."
   (make-music 'DoublePercentEvent
               'length (ly:music-length note)))


  
\score{{ \label #'oscarwoods
\transpose d d' {
\time 6/8 \key g \major

  b8 a8 g8 b8 a8 g8 b4 \grace{c'8} d'8 d'8 e'8 d'8
  b8 a8 g8 b8 a8 g8 a4 a8 a4.
  b8 a8 g8 b8 a8 g8 b8 c'8 d'8 e'4.
  d'4 g'8 d'8 b8 g8 a4. g4. \bar "||" \break
  b4 d'8 d'4 b8 c'4 e'8 e'4 c'8
  b4 d'8 d'4 b8 c'4 a8 a4.
  b4 d'8 d'4 b8 c'4 e'8 e'4.
  d'4 g'8 d'8 b8 g8 a4. g4. \bar "|."
  
}}
\header{
piece = "Oscar Woods' Jig"
subtitle = "Tiger Smith's Jig"
opus = "WFS 13-07 01"
}}
\markuplist{
    "Into..."
}

\score{{ 
\transpose d d' {
\time 6/8 \key g \major
  
  g4 b8 d'4 d'8 g'8 fis'8 e'8 d'4.
  c'8 e'8 c'8 b8 d'8 b8 a8 g8 a8 b4 a8
  \makePercent s2. \makePercent s2.
  \makePercent s2. a8 g8 a8 g4. \bar "||" \break
  
  b4. b4.-> b8 a8 b8 c'4. b4 c'8 d'4 c'8 b4 a8 b4 g8
  \makePercent s2.   \makePercent s2.
  
  <<
    { d'4 g'8 d'8 b8 g8 a4. g4. }
    \new Staff \ossia
    { b4 c'8 d'4 d'8 c'8 b a g4. }
  >>  
  
  \bar "|."  
  
}}
\header{
piece = "Captain Lanoe's Quick March"
opus = "WFS 13-07 02"
}}
\markuplist{
  "Into..."
}

\score{{
\transpose d d' {
\time 6/8 \key d \major
  
  d'4 a8 a4 fis8 g8 a8 b8 a4.
  b8 cis'8 d'8 e'8 fis'8 g'8 fis'8 e'8 d'8 cis'8 b8 a8
  \makePercent s2.   \makePercent s2.
  \makePercent s2. a8 d'8 cis'8 d'4. \bar "||" \break
  e'4 a8 a4 fis'8 e'8 fis'8 g'8 fis'4.
  e'8 fis'8 g'8 fis'8 e'8 d'8 cis'8 d'8
  << \new Voice { \voiceOne e'8 } \new Voice { \voiceTwo b8 } \oneVoice >>
  a4.
  b8 g8 b8 a8 fis8 a8 b8 g8 b8 a8 fis8 a8
  b8 cis'8 d'8 e'8 fis'8 g'8 a8 d'8 cis'8 d'4. \bar "|."
  
}}
\header{
piece = "The Moon and Seven Stars"
opus = "WFS 13-07 03"
}}


\score{{
\transpose d d' {
\time 4/4 \key d \major

  fis4 a4 g4 b4 a4 fis'4 fis'8 e'8 fis'4
  <<
    { g4 e'4 e'8 d'8 e'4 fis4 d'4 d'8 cis'8 d'4 }
    \new Staff \ossia
    { \key d \major g4 e'8 d'8 cis'8 b8 a8 g8 fis4 d'8 cis'8 d'2 }
  >>
  
  \makePercent s1  \makePercent s1
  g'4 e'4 e'8 g'8 fis'8 e'8 d'4 fis'4 d'2 \bar "||" \break
  \key g \major
  g'4 fis'4 e'8 fis'8 g'8 e'8 d'4 b4 b8 a8 b4
  c'4 a4 a8 g8 a4 b4 g4 g2
  \makePercent s1  \makePercent s1
  c'4 a4 a8 c'8 b8 a8 g4 \afterGrace b4 a8 g2 \bar "|."
  
}}
\header{
piece = "Jenny Lind Polka"
opus = "WFS 13-07 04"
}}




\score{{
\transpose d d' {
\time 3/4 \key g \major
  
  \partial 4. d8 g8 a8
  b4 b4 c'4 d'2 g'8 fis'8
  \afterGrace e'4. {c'8 e'8} fis'8 g'8 e'8 d'4.
  \makePercent s4.
  \makePercent s2.
  \makePercent s4.
  e'8 c'8 a8
  g2 a4 g2 \bar "||" \break a8 b8
  c'4. d'8 c'8 b8 a2
  << \new Voice { \voiceOne e'4 } \new Voice { \voiceTwo b8 c'8 } \oneVoice >>
  d'4. e'8 d'8 c'8 b2 g'8 fis'8
  e'8 c'8 e'8 fis'8 g'8 e'8 d'4.
  d8 g8 a8 b4. c'8 \afterGrace a4 fis4 g2. \bar "|."
  
}}
\header{
piece = "Michael Turner's Waltz"
opus = "WFS 13-07 05"
}}


\score{{
\transpose d d' {
\time 4/4 \key g \major
  
  b4 g4 d4 g4 fis8 g8 a8 b8 c'8 e'8 d'8 c'8
  b4 g4 d4 g4
  fis8 g8 a8 fis8 g2 
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve
  \bar "||" \break
  b4. c'8 d'4 d'4 b4 c'4 d'2 e'4 d'4 c'4
  b4 a4 b4 c'8 e'8 d'8 c'8
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve
  \bar "|."
    
}}
\header{
piece = "Getting Upstairs"
opus = "WFS 13-07 06"
}}



\score{{
\transpose d d' {
\time 4/4 \key d \major

    d4 fis8 a8 d'4 d'4 b8 g8 b8 d'8 a2
    cis'4 \grace a8 cis'8 e'8 d'4 \grace a8 d'8 fis'8 e'8 cis'8 d'8 b8 a8 g8 fis8 e8
    \makePercent s1 \makePercent s1
    <<
    { b4 \grace g8 b8 d'8 cis'4 \grace a8 cis'8 e'8 }
    \new Staff \ossia
    { \key g \major b8 cis'8 d'4 cis'8 d'8 e'4 }
  >>
    
    d'2 d'2 \bar "||" \break
    
    e'8 cis'8 a4 a4 e'4 fis'8 d'8 a4 a2
    g'4 fis'4 e'4 d'4 cis'8 d'8 cis'8 b8 a8 g8 fis8 e8
    \makeDoublePercent s\breve
    \makeDoublePercent s\breve
    

}}
\header{
piece = "Sheffield Hornpipe"
opus = "WFS 13-07 07"
}}

\score{{
\transpose d d' {
\time 6/8 \key g \major
  \repeat volta 2 {
  \partial 4. d8 e8 fis8
  g4 fis8 g4 b8 a4 g8 e4 d8 g4 b8 d'4 g'8 e'4. d'8 e'8 fis'8
  g'4 fis'8 g'4 d'8 e'4 d'8 b4 g8 }
  \alternative { { a4 b8 a4 g8 e4. s4.}
  {a8 b8 a8 g4 fis8 g4.} } \bar "||" \break 
  b4 d'8
  g'4 fis'8 e'4 g'8 fis'4 e'8 d'4 fis'8 e'4 d'8 e'4 fis'8 e'4 d'8 b4 g8
  g'4 fis'8 g'4 d'8 e'4 d'8 b4 g8
  a4 b8 a4 g8 e4. \bar "|."
  
}}
\header{
piece = "Off to California"
opus = "WFS 13-07 08"
meter = "A1 A2 B A2"
}}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  
  g4. a8 b4 b4 c'4 b4 a4 c'4 b4 a4 g4 fis4 e2 d2
  \makePercent s1 \makePercent s1
  b4 g4 a4 fis4 g2 g2 \bar "||" \break
  d'4 c'8 b8 a4 b4 c'4 b8 a8 g8 a8 b4 a4 g4 fis4 g4 a2 a2
  \makePercent s1 \makePercent s1
  a4 g4 g4 fis4 g2 g2 \bar "||" \break 
  bes4 a8 g8 bes4 a8 g8 fis4 g4 a2 d4 e4 fis4 g4 a4 bes4 a4 g4
  \makePercent s1 \makePercent s1
  d4 e4 fis4 g4 g4 fis4 g2 \bar "|."
   
}}
\header{
piece = "Horses Brawl"
opus = "WFS 13-07 09"
}}
\markuplist{
    "Featured, with dance instructions, in Arbeau's Orchesographie (1589)"
}

\score{{
\transpose d d' {
\time 4/4 \key d \major
  
  \partial 4 a8 g8
  fis8 d8 fis8 a8 d'4 d'4 d'8 fis'8 e'8 d'8 d'8 cis'8 b8 a8
  b4 g8 b8 a4 fis8 a8 g4 e4 e4 a8 g8
  \makePercent s1 \makePercent s1
  d'4 d'4 e'8 g'8 fis'8 e'8 fis'4 d'4 d'2 \bar "||" \break
  
  a'4 fis'8 a'8 g'4 e'8 g'8 fis'4 d'8 fis'8 e'8 cis'8 a8 b8
  c'4-> c'4-> e'8 fis'8 g'8 e'8 c'4-> c'4-> e'8 fis'8 g'8 e'8
  \makePercent s1 \makePercent s1
  d'4 d'4 e'8 fis'8 g'8 e'8 fis'4 d'8 cis'8 d'2 \bar "|."
  
}}
\header{
piece = "Staten Island Ferry"
opus = "WFS 13-07 10"
}}

\score{{
\transpose d d' {
\time 4/4 \key d \major
  \partial 4 a4
  d'4 fis'8 e'8 d'8 cis'8 d'8 b8 a8 b8 a8 g8 fis4 a4
  d'4 e'8 fis'8 g'8 fis'8 g'8 fis'8 e'4 a'4 a'4 a4
  \makePercent s1   \makePercent s1
  b4 g'8 fis'8 e'8 d'8 cis'4 d'2 d'4 \bar "||" \break
  fis'8 g'8 a'4 a'8 g'8 fis'8 g'8 fis'8 e'8 d'8 e'8 d'8 cis'8 b2
  g'4 g'8 fis'8 e'8 fis'8 e'8 d'8 cis'8 d'8 cis'8 b8 a2
  d'4 d'4 cis'8 e'8 cis'8 a8 d'4 d'4 cis'8 e'8 cis'8 a8
  d'4 fis'4 g'8 fis'8 e'4 d'2. \bar "|."
}}
\header{
piece = "Enrico"
opus = "WFS 13-07 11"
}}

\score{{
\transpose d d' {
\time 6/8 \key g \major
  d4 g8 g8 fis8 g8 b4 g8 g8 fis8 g8
  e4 a8 a4 b8 c'8 b8 a8 g8 fis8 e8
  \makePercent s2.   \makePercent s2.
  fis8 e8 d8 d8 e8 fis8 g8 a8 b8 a4 g8
  \bar "||" \break
  g4 b8 c'4 e'8 d'4 e'8 d'8 b8 g8
  g4 b8 c'4 e'8 d'8 b8 g8 a4.
  \makePercent s2.  \makePercent s2.
  g4 g8 b8 a8 g8 fis8 e8 fis8 g4. 
  \bar "||" \break
  c'4 a8 a8 g8 a8 b4 g8 g4 g8
  fis4 g8 a4 b8 c'4 a8 fis4 d8
  \makePercent s2.  \makePercent s2.
  fis8 e8 d8 d8 e8 fis8 g8 a8 b8 a4 g8
  \bar "|."
  
  
}}
\header{
piece = "Paddy Carey's"
opus = "WFS 13-07 12"
}}
\markuplist{
  Into...
}

\score{{
\transpose d d' {
\time 6/8 \key g \major

  g4 d8 e4 d8 g4 d8 e4 d8
  g8 a8 b8 c'4 b8 a4 g8 fis8 e8 d8 
  \makePercent s2. \makePercent s2.
  g8 a8 b8 c'4 b8 a8 g8 fis8 g4.
  \bar "||" \break
  g8 a8 b8 c'4. b4. a4. 
  a8 b8 c'8 d'4. c'4. b4.
  \makePercent s2. \makePercent s2.
  b8 c'8 d'8 b8 a8 g8 b4 a8 g4.
  \bar "|."

}}
\header{
piece = "Spirit Of The Dance"
opus = "WFS 13-07 13"
}}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  g4. a8 b4 b4 c'4 b4 c'4 a4
  g4. a8 b4 g4 fis4 a4 fis4 d4
  \makePercent s1 \makePercent s1
  b4 d'4 c'8 b8 a8 g8 fis4 a4 fis4 d4
  \bar "||" \break
  e8 g8 c'4 c'4. g8 e4 c'4 g4 e4
  fis8 a8 d'4 d'4. a8 fis4 d'4 a4 fis4
  \makePercent s1 \makePercent s1
  b4 d'4 c'8 b8 a8 g8 fis4 a4 fis4 d4
  \bar "|."
}}
\header{
piece = "Ffiddle-Ffaddle"
opus = "WFS 13-07 14"
}}

\score{{
\transpose d d' {
\time 4/4 \key d \major
  d'4 a4 c'4. b8 a4 fis4 g2
  a4 b4 a8 b8 a8 g8 fis4 e4 e2
  \makePercent s1 \makePercent s1
  a4 b4 a8 b8 a8 g8 fis4 e4 d2
  \bar "||" \break
  g4 e4 b8 g8 e8 b8 g8 e8 b4 b4 g4
  fis4 a4 a8 fis8 d8 a8 fis8 d8 a4 a2
  \makePercent s1 \makePercent s1
  a4 d'4 a8 b8 a8 g8 fis4 e4 d2
  \bar "|."
}}
\header{
piece = "La Roulante"
subtitle = "/ L.N.B. Polka"
opus = "WFS 13-07 15"
}}

\score{{
\transpose d d' {
\time 6/8 \key e \minor
  g8 fis8 g8 a8 g8 a8 b4 g8 e4 b8
  c'4 b8 a8 b8 c'8 d'8 c'8 b8 a4.
  g8 fis8 g8 a8 g8 a8 b4 g8 e4 g8
  fis4 b8 b,8 cis8 dis8 e4. e8
  \bar "||" \break
  b8 c'8 d'4 d'8 d'4 b8 c'8 b8 c'8 a8 b8 c'8
  b4 b8 b4 g8 b8 a8 g8 fis4 b8
  e4 g8 fis8 g8 a8 g4 b8 a8 b8 c'8
  b4 g8 b,8 cis8 dis8 e4. e8
  \bar "|."

}}
\header{
piece = "Clapton ?"
opus = "WFS 13-07 16"
}}

\score{{
\transpose d d' {
\time 4/4 \key e \minor
    e4 e8 fis8 g4 a4 b8 c'8 b8 a8 b2
    a4 fis4 fis8 g8 a8 fis8 g4 e4 e4 d4
    \makePercent s1 \makePercent s1
    \makePercent s1 \makePercent s2. g4
    \bar "||" \break
    fis4 fis8 g8 a4 c'4 b4 g8 a8 b2
    e'4 g'8 e'8 d'4 g8 a8 b4 a4 a2
    \makePercent s1 \makePercent s1
    \makePercent s1 b4-- c'4-- b2--
    \bar "|."
}}
\header{
piece = "?"
opus = "WFS 13-07 17"
}}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  d4 g4 d4 g8 b8 c'4 c'4 a2
  fis8 g8 a4 fis8 g8 a4 g8 b8 d'8 e'8 d'2
  e'4 c'8 e'8 d'4 b4 c'8 b8 a8 b8 a4 g4
  d4 g4 fis8 g8 a8 b8 a4 g4 g4
  \bar "||"\break
  b8 c'8 d'4 b4 c'4 e'4 e'4 a4 a4
  b8 c'8 d'4 b4 c'8 d'8 e'4 e'8 d'8 c'8 b8 a2
  g8 a8 b8 c'8 d'4 b4 c'8 b8 a8 b8 a4 g4
  d4 g4 fis8 g8 a8 b8 a4 g4 g2
  \bar "|."
  
}}
\header{
piece = "?"
opus = "WFS 13-07 18"
}}


\score{{
\transpose d d' {
\time 4/4 \key g \major
  d'4 b8 a8 g4 g4 a4 b8 a8 g4 d4
  e8 d8 e8 fis8 g4 a8 b8 c'4 b4 b4 a4
  \makePercent s1 \makePercent s1
  e8 d8 e8 fis8 g4 a8 c'8 b4 a4 g2
  \bar "||" \break
  d'4 e'8 fis'8 g'8 fis'8 e'8 d'8 e'4 e'4 e'2
  d'4 b4 b4 a8 g8 fis8 g8 a8 b8 a2
  \makePercent s1 \makePercent s2. d'4
  e'8 fis'8 g'4 fis'8 g'8 a'4 g'2 g'2
  \bar "|."
}}
\header{
piece = "Three around Three"
opus = "WFS 13-07 19"
}}
\markuplist{
  Into...
}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  g4 g4 fis8 g8 a8 fis8 g8 a8 b8 c'8 d'4 b8 d'8
  e'4 c'8 e'8 d'4 b4 a8 b8 a8 g8 e4 d4
  \makePercent s1 \makePercent s1
  e'4 c'8 e'8 d'8 b8 g8 b8 a4 fis4 g4
  \bar "||" \break
  fis'4 g'4 e'8 g'8 fis'4 d'4 e'4 c'8 e'8 d'4 b4
  e'4 c'8 e'8 d'4 b4 a8 b8 a8 g8 e4 d4
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve
  \bar "|."
}}
\header{
piece = "Great North Run '86"
opus = "WFS 13-07 20"
}}
\markuplist{
  Into...
}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  \partial 4 g8 a8 
  b4 d'8 b8 a8 g8 a4 g8 a8 b8 c'8 d'4 e'8 fis'8
  g'8 fis'8 g'8 e'8 d'8 b8 g8 d'8 e'4 a4 a4 g8 a8
  \makePercent s1 \makePercent s1
  g'8 fis'8 g'8 e'8 d'8 b8 g8 a8 b4 a4 g4 
  \bar "||" \break
  d'4
  e'8 d'8 e'8 fis'8 g'8 fis'8 g'8 e'8 d'8 b8 g8 b8 d'4 d'4
  e'8 d'8 e'8 fis'8 g'8 fis'8 g'8 e'8 d'8 b8 g8 b8 a4 g8 a8
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve
  \bar "|."
}}
\header{
piece = "Hesleyside Reel"
opus = "WFS 13-07 21"
}}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  \partial 4 d'8 c'8
  b4 b8 c'8 a4 a8 b8 g4 g4 g4 a8 b8
  c'8 b8 c'8 d'8 e'8 d'8 c'8 b8 a4 a4 a4 d'8 c'8
  \makePercent s1 \makePercent s1
  c'8 b8 a8 g8 fis8 g8 a8 fis8 g2 g4
  \bar "||" \break
  b8 c'8 d'4 g'8 fis'8 e'4 e'4 d'8 c'8 b8 c'8 a4
  b8 c'8 d'4 g'8 fis'8 e'8 d'8 c'8 b8 a4 a4 a4 b8 c'8
  \makePercent s1 \makePercent s2. d'8 c'8
  b4 b8 c'8 a4 a8 b8 g4 g4 g4 
  \bar "||" \break
  b8 c'8 d'4 d'8 d'8 d'4 g'4 d'4 d'8 d'8 d'4 g'4
  d'4 d'4 e'8 d'8 c'8 b8 a4 a4 a4 b8 c'8
  \makePercent s1 \makePercent s1
  e'8 d'8 c'8 b8 a8 c'8 b8 a8 g2 g4
  \bar "|."
  
  
}}
\header{
piece = "Galopede"
opus = "WFS 13-07 22"
}}


%{

\score{{
\transpose d d' {
\time 6/8 \key g \major
  b8 a8 g8 e'8 d'8 b8 a8 g8 a8 b4 g8
  d4 g8 b4 g8 a8 g8 a8 b4 g8
  \makePercent s2. \makePercent s2.
  \makePercent s2. a8 b8 a8 g4.
  \bar "||" \break
  c'4. e'4. g'4 f'8 e'8 d'8 c'8
  b4 g8 d4 g8 a8 g8 a8 b4 g8
  \makePercent s2. \makePercent s2.
  \makePercent s4. d8 g8 d'8 c'8 b8 a8 g4.
  \bar "||" \break
  d'4. fis'4. a'4 fis'8 d'8 e'8 c'8
  b4 g8 d4 g8 d'4 c'8 b8 a8 g8
  \makePercent s2. \makePercent s2.
  \makePercent s4. d8 g8 d'8 c'8 b8 a8 g4.
  \bar "|."
}}
\header{
piece = "Monsal Jig"
}}
\score{{
\transpose d d' {
\time 6/8 \key g \major
  
}}
\header{
piece = "?"
}}
\markuplist{
}
%}

