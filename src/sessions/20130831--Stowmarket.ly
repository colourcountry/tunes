\version "2.16.0"

\layout { 
  indent = 0.0\cm
  \context { \Score \remove "Bar_number_engraver" }	
  \context { \Staff \remove "Time_signature_engraver" }
}

\layout {
  indent = 0.0\cm
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

%{ Barn session recording. %}


\score{{
\transpose d d' {
\time 2/2 \key g \major
  g8 a8 b8 c'8 d'4 b4 c'4 e'4 d'2
  g8 a8 b8 c'8 d'4 b4 c'4 e'4 a2
  \makePercent s1 \makePercent s2
  d'4 e'8 fis'8
  g'4 b4 c'8 e'8 d'8 c'8 b4 g4 g2
  \bar "||" \break
  g'4 g'4 g'8 a'8 g'8 fis'8 e'4 c'4 c'2
  a'4 a'4 a'8 b'8 a'8 g'8 fis'4 d'4 d'4 e'8 fis'8
  g'8 a'8 g'8 fis'8 e'4 a'8 g'8 fis'8 g'8 fis'8 e'8 d'4 e'8 fis'8
  g'4 b4 c'8 e'8 d'8 c'8 b4 g4 g2
  \bar "|."
}}
\header{
piece = "?"
opus = "EATMD 13-01 01"
}}
\markuplist{ "Into..." }


\score{{
\transpose d d' {
\time 2/2 \key g \major
  c'2 e4. fis8 g4 g4 g2
  a4 a8 b8 c'8 b8 c'8 d'8 e'4 e'4 a2
  a4 a8 b8 c'8 b8 c'8 d'8 e'8 d'8 e'8 fis'8 g'4 fis'8 g'8
  a'8 fis'8 d'8 fis'8 e'8 g'8 e'8 cis'8 a2.
  \bar "||" \break e'8 fis'8
  g'4 g'4 g'8 fis'8 e'8 d'8 cis'8 d'8 e'8 fis'8 g'4 fis'4
  e'4 a'4 a'2 e'4 a'4 a'4 e'8 fis'8 \noBreak
  g'4 g'4 g'8 fis'8 e'8 d'8 cis'8 d'8 e'8 fis'8 g'4 fis'8 g'8
  a'8 fis'8 d'8 fis'8 e'8 g'8 e'8 cis'8 a2.
  \bar "|."
}}
\header{
piece = "Radstock Jig"
opus = "EATMD 13-01 02"
}}

\score{{
\transpose d d' {
\time 6/8 \key d \major
  fis4 fis8 fis8 e8 d8 a4 a8 a4 fis8
  g4 g8 g8 fis8 e8 b4. b4 d'8
  cis'4 bis8 cis'4 d'8 e'4 cis'8 b4 a8
  d'4 cis'8 d'4 e'8 fis'8 e'8 d'8 cis'8 b8 a8
  \makePercent s2. \makePercent s2.
  \makePercent s2. \makePercent s4. cis'4.
  d'4 d'8 d'8 cis'8 b8 a4 a8 a8 g8 fis8
  e8 fis8 g8 a8 b8 cis'8 d'8 a8 b8 cis'8 d'8 e'8
  \bar "||" \break
  fis'4. fis'4. fis'8 e'8 d'8 a4.
  d'8 cis'8 d'8 e'4 d'8 cis'4. b4.
  g'4. g'4. g'8 fis'8 e'8 b4.
  cis'4 bis8 cis'4 d'8 e'4 cis'8 b4 a8
  \makePercent s2. \makePercent s2.
  \makePercent s2. \makePercent s2.
  g'4 g'8 g'8 fis'8 e'8 d'4 d'8 d'8 cis'8 b8
  a4 a8 b4 cis'8 d'4.   \bar "||" \break
  c'4.
  b4. b4. c'4. cis'4. d'4 cis'8 d'4 e'8 d'2.
  b4 c'8 cis'4 d'8 e'4. d'4. fis2. fis4. a4 b8
  c'4. c'4. c'4 b8 a4 b8 c'4. c'4. c'4 b8 c'4 d'8
  fis'4. e'4. d'4. a4. ais2. b4. s4.
  \makePercent s2. \makePercent s2.
  \makePercent s2. \makePercent s2.
  b4 c'8 cis'4 d'8 e'4. d'4. fis'2. fis'4. e'4 fis'8
  g'4 g'8 g'8 fis'8 e'8 g'4 g'8 g'8 fis'8 e'8
  d'4 d'8 d'8 cis'8 d'8 e'4. c'4 b8
  a4 a8 b8 ais8 b8 c'8 d'8 e'8 d'8 e'8 fis'8
  g'4 d'8 e'8 d'8 b8 g4.
  \bar "|." a4.
}}
\header{
piece = "Britannia Two Step"
opus = "EATMD 13-01 03"
}}
\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 6/8 \key g \major
  \repeat volta 2 {
  b4 b8 b8 a8 g8 b4 b8 b8 a8 g8
  g8 a8 g8 fis4 g8 a4.~a4 d'8
  fis'4 fis'8 fis'8 e'8 d'8 fis'4 fis'8 fis'8 e'8 d'8
  } \alternative {
    {  d'8 cis'8 d'8 e'4 d'8 b4.~b4 d8 \break }
    {  d'8 cis'8 d'8 e'4 fis'8 g'8 }
  }
  \bar "||"
  d'8 e'8 fis'8 g'8 a'8
  \repeat volta 2 {
  b'4 a'8 g'8 fis'8 e'8 d'4 b8 g4 a8
  b4 b8 b8 a8 b8 c'4.~c'4 d'8
  fis'4 fis'8 fis'8 e'8 d'8 fis'4 fis'8 fis'8 e'8 d'8
  } \alternative {
    { d'8 cis'8 d'8 e'4 d'8 b4 d'8 g'4 a'8 }
    { d'8 cis'8 d'8 e'4 fis'8 g'4. }
  }
  \bar "|."
  d'4.
}}
\header{
piece = "?"
opus = "EATMD 13-01 04"
}}

\score{{
\transpose d d' {
\time 2/2 \key d \major
  \partial 4 a4
  d'4. cis'8 d'4 e'4 fis'4. e'8 d'4 cis'4
  b4 a4 b8 cis'8 d'8 b8 a4 g4 fis4 a4
  \makePercent s1 \makePercent s1
  b4 a4 b4 cis'4 d'2 d'4 \bar "||" \break a4
  b4 a4 fis4 a4 b4 a4 fis4 \afterGrace d'4 d'8 d'4 \afterGrace cis'4 cis'8 cis'4
  \afterGrace b4 b8 b4 \afterGrace a4 a8 a4
  \afterGrace d'4 d'8 d'4 \afterGrace cis'4 cis'8 cis'4
  \afterGrace e'4 e'8 e'4 \afterGrace d'4 d'8 d'4 fis'4
  fis'4 e'4 b4 cis'4 d'2 d'4
  \bar "|."
}}
\header{
piece = "The Sloe"
subtitle = "Hardcore 48-03"
opus = "EATMD 13-01 05"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 2/2 \key d \major
  \partial 4 a4
  d'4 cis'4 b4 a4 g4 fis4 e4 d4
  d8 e8 fis8 g8 a4 fis4 fis4 e4 e4 a4
  \makePercent s1 \makePercent s1
  d8 e8 fis8 g8 a4 fis'4
  \time 3/2 e'4 cis'8 d'8 e'4 d'8 cis'8 d'4
  \bar "||" \break
  e'4
  \time 2/2
  fis'4 fis'8 fis'8 fis'4 fis'4 g'8 fis'8 e'8 d'8 e'4 e'4
  fis'4 fis'8 fis'8 fis'4 fis'4 e'8 d'8 cis'8 b8 a4 e'4
  \makePercent s1 \makePercent s1
  fis'4 d'4 e'4 cis'4 d'2 d'4
  \bar "|."
  }}
\header{
piece = "Herbert Smith's Four-hand Reel"
opus = "EATMD 13-01 06"
}}

\score{{
\transpose d d' {
\time 6/8 \key d \major
  \partial 8 a8
  d'4 d'8 fis'4 a'8 g'8 fis'8 g'8 e'4 a'8
  fis'4 d'8 b4 e'8 cis'8 b8 cis'8 a4 a8
  \makePercent s2. \makePercent s2.
  a'8 fis'8 d'8 g'8 e'8 cis'8 d'4.~d'4
  \bar "||" \break a8
  d'4 d'8 cis'8 d'8 cis'8 b4.~b4 b8
  e'4 e'8 d'8 e'8 d'8 cis'4.~cis'4 a8
  d'8 cis'8 d'8 e'8 d'8 e'8 fis'8 e'8 fis'8 g'8 fis'8 g'8
  a'8 fis'8 d'8 g'8 e'8 cis'8 d'4.~d'4
  \bar "|."

}}
\header{
piece = "The Burdett"
subtitle = "John Clare JC.044"
opus = "EATMD 13-01 07"
}}

\markuplist{ 
  "Into..." }

\score{{
\transpose d d' {
\time 6/8 \key d \major
  d4 fis8 a4 d'8 fis'4 d'8 a4 fis8
  g4 b8 e'4 d'8 cis'8 b8 a8 g8 fis8 e8
  \makePercent s2. \makePercent s2.
  g4 e'8 cis'8 b8 a8 cis'4. d'4.
  \bar "||" \break 
  a4 cis'8 e'4 cis'8 a4 d'8 fis'4 d'8
  a4 e'8 g'4 e'8 fis'8 e'8 d'8 cis'8 b8 a8
  d'4 a8 e'4 a8 fis'4 a8 g'4 a8
  fis'8 e'8 d'8 cis'8 b8 cis'8 cis'4. d'4.
  \bar "|."

}}
\header{
piece = "Sadler's Balloon"
subtitle = "John Clare JC.096"
opus = "EATMD 13-01 08"
}}


\score{{
\transpose d d' {
\time 2/2 \key g \major
  g4. g8 g4 g4 fis8 g8 a8 fis8 g4 a4
  b4 b8 g8 c'4 c'8 a8 b4 b8 g8 a2
  \makePercent s1 \makePercent s1
  fis8 g8 a8 b8 a8 g8 fis8 e8 d2.
  \bar "||" \break b8 c'8
  d'8 c'8 b8 a8 g8 fis8 e8 d8 e4 c4 c2
  e'8 d'8 c'8 b8 a8 g8 fis8 e8 fis4 d4 d4 b8 c'8
  d'4 d'8 b8 e'4 e'8 c'8 d'4 d'8 b8 e'4 e'8 c'8
  d'8 g'8 fis'8 e'8 d'8 c'8 b8 a8 g8 a8 g8 fis8 g2
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 09"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 2/2 \key d \major
  a8 g8 fis8 g8 a4. a8 b8 cis'8 d'8 e'8 d'8 cis'8 b8 a8
  d'8 e'8 fis'8 d'8 b4 cis'8 d'8 e'8 fis'8 g'8 e'8 d'8 cis'8 b8 a8
  \makePercent s1 \makePercent s1
  d'8 e'8 fis'8 d'8 b4 g'4 fis'4 e'4 d'4
  \bar "||" \break d'8 e'8
  fis'4. g'8 a'8 g'8 fis'4 e'4. fis'8 g'8 fis'8 e'4
  d'8 e'8 fis'8 d'8 b4 cis'8 d'8 e'8 fis'8 g'8 e'8 d'8 cis'8 b8 a8
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve  
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 10"
}}

\score{{
\transpose d d' {
\time 2/2 \key g \major
  \partial 4
  b8 c'8 d'4 g4 g4 a8 b8 c'4 e4 e4 a8 g8
  fis8 g8 a8 b8 c'8 b8 c'4 e'4 d'4 d'4 b8 c'8
  \makePercent s1 \makePercent s1
  fis8 g8 a8 b8 c'8 a8 fis4 a4 g4 g2
  \bar "||" \break 
  g'4 g'4 g'4 a'8 g'8 fis'4 e'4 e'2
  c'4 c'4 c'8 b8 c'8 d'8 e'4 d'4 d'2
  \makePercent s1 \makePercent s1
  fis8 g8 a8 b8 c'8 a8 fis4 a4 g4 g2
  \bar "|."  
}}
\header{
piece = "Hills of Tara"
opus = "EATMD 13-01 11"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 2/2 \key g \major
  g4 g4 fis8 g8 a8 fis8 g4 g4 fis8 g8 a8 fis8
  g4 a8 b8 c'8 b8 a8 g8 fis8 g8 a8 fis8 d2
  \makePercent s1 \makePercent s1 \makePercent s1
  fis8 g8 a8 fis8 g2
  \bar "||" \break
  d'4 d'4 d'4. e'8 d'8 c'8 b8 a8 g2
  a4 a4 d4 d4 a4 b8 c'8 d'2
  \makePercent s1 \makePercent s1
  a4 a4 d4 e8 fis8 g2 g2
  \bar "|."  
}}
\header{
piece = "Fred Pigeon's"
opus = "EATMD 13-01 12"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 2/2 \key g \major
  g8 fis8 g8 a8 b8 a8 b8 c'8 d'4 d'4 b2
  c'4 a4 a2 fis4 d4 d2
  \makePercent s1 \makePercent s1
  c'4 a4 fis4 d4 fis4 g4 g2
  \bar "||" \break
  b4 g8 g8 g4 g4 g2. a4
  b4 g8 g8 g4 g4 a2. a4
  b4 g8 g8 g4 fis4 e4 c'4 c'2
  b8 d'8 c'8 b8 a4 a4 g2
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 13"
}}

\score{{
\transpose d d' {
\time 6/8 \key g \major
  g'8 fis'8 g'8 d'4 b8 c'8 d'8 e'8 d'4.
  c'8 a'8 c'8 b8 g'8 b8 a8 d'8 c'8 b8 a8 g8
  \makePercent s2. \makePercent s2.
  c'8 a'8 fis'8 g'8 d'8 b8 c'8 a8 fis8 g4.
  \bar "||" \break
  \repeat volta 2 {
  b8 a8 b8 g8 a8 b8 c'8 b8 c'8 a8 b8 c'8
  b8 d'8 c'8 b8 a8 g8 fis8 d8 e8 fis8 g8 a8
  }
  \alternative {
    {
      \makePercent s2. 
      c'8 b8 c'8 e8 d8 c8 
      b,8 c8 d8 e8 fis8 g8 a8 g8 fis8 g4 a8
    }{
      \makePercent s2. 
      c'8 a8 fis8 d8 e8 c8  
      b,8 c8 d8 e8 fis8 g8 a8 b8 c'8 d'8 e'8 fis'8
    }
  }
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 14"
}}
\markuplist{ "Into..."
}
\score{{
\transpose d d' {
\time 6/8 \key g \major
  d'4 b8 d'8 c'8 a8 g4 g8 g8 fis8 g8
  a8 fis8 d8 d8 e8 fis8 g8 b8 d'8 g'8 fis'8 e'8
  \makePercent s2. \makePercent s2.
  a8 fis8 d8 d8 e8 fis8 g4 \grace{d8} b8 g4.
  \bar "||" \break
  a8 d'8 fis'8 fis'8 e'8 fis'8 g'8 d'8 b8 d'8 b8 g8
  \makePercent s2. \makePercent s4. g8 b8 d'8
  e'4 \grace{c'8} e'8 g'8 fis'8 e'8 d'4 \grace{b8} d'8 g'8 d'8 b8
  d'8 c'8 a8 c'8 b8 g8 b4. a4.
  \bar "|."  
}}
\header{
piece = "Doncaster Races"
subtitle = "Hardcore 57-03"
opus = "EATMD 13-01 15"
}}

\score{{
\transpose d d' {
\time 6/8 \key g \major
  \repeat volta 2 {
  g4 g8 g8 a8 b8 a8 fis8 d8 d8 e8 fis8
  g4 b8 d'4 b8 d'8 e'8 fis'8 g'4 fis'8
  } \alternative {
    {
      e'4 c'8 c'8 d'8 e'8 d'4 b8 g8 a8 b8
      c'4 b8 a4 g8 fis8 g8 a8 d8 e8 fis8
    }
    {
      e'4 c'8 g'8 fis'8 e'8 e'8 d'8 c'8 b8 a8 g8
      fis8 g8 a8 d8 e8 fis8 g4. g4
    }
  }
  \bar "||" b8
  b8 e'8 e'8 e'4 fis'8 g'4.~g'4 g'8
  fis'4 b8 a'8 g'8 fis'8 e'4.~e'4 a8
  a8 d'8 d'8 d'4 e'8 fis'4.~fis'4 g'8
  a'8 b'8 a'8 g'8 fis'8 e'8 d'4 b8 c'8 b8 a8
  \makeDoublePercent s1.
  \makeDoublePercent s1.
  \makeDoublePercent s1.
  \makeDoublePercent s1.
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 16"
}}

\score{{
\transpose d d' {
\time 2/2 \key g \major
  \partial 4 g8 a8
  b8 c'8 d'4 g4 g'4 e'2. g'4 d'4 d'8 e'8 d'4 b4
  a8 g8 fis8 g8 a4 b4 g4 d2 b4 c'4 a4 d'8 c'8 b8 a8
  b4 \grace{c'8} d'4 a4 \afterGrace b4 a8 g2.
  \bar "||" \break g8 a8
  b4 g4 c'4 a4 b4 g4 g4. a8
  b4 g4 d'4 b4 a8 g8 fis8 g8 a4 b4
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve
  \bar "||" \break
  g'8 fis'8 e'8 fis'8 g'4 a'4 g'4 fis'4 e'4 d'4
  b8 c'8 d'4 e'8 fis'8 g'4 g4 fis4 e4 d4
  e4 c4 c'4 a4 b4 g4 d'8 c'8 b8 a8  
  \makeDoublePercent s\breve
  \bar "|."  
}}
\header{
piece = "The Shepherd And Shepherdess"
opus = "EATMD 13-01 17"
}}

\score{{
\transpose d d' {
\time 3/4 \key g \major
  \repeat volta 2 {
  \partial 4 d4

  b4. c'8 b4 a4 d'4 b4 g4. a8 g4 fis4 b4 g4
  e4. g8 e4 d4 b4 g4 }
  \alternative {
    {  g4 fis4 g4 a2 s4 }
    {  a4 e4 fis4 g2 }
  }
  \bar "||" \break 
  \repeat volta 2 {
  fis4
  e2 d4 d4 b4 g4 a4 b4 c'4 b4 a4 g4
  e4 c'4 e4 d4 b4 g4
  } \alternative {
  { a2 g4 fis4 e4 d4 }
  { a4 e4 fis4 \afterGrace g2 g4 } }
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 18"
}}

\score{{
\transpose d d' {
\time 3/4 \key g \major
  \partial 4 d4
  e4 g4 e4 d4 g4 a4
  b8 d'4. b4 a2 b8 a8
  g4 e4 e4 d4 g4 a4 b4 g4 g4 g2
  \bar "||" \break a4
  b4. a8 b8 c'8 d'2 b4 a4 g4 a4 b4 c'4 d'4
  e'4 d'4 b4 a4 g4 a4 b4 a4 g4 e2 d4
  \makeDoublePercent s1.
  \makeDoublePercent s1.
  \bar "|."  
}}
\header{
piece = "Sherborne Waltz"
subtitle = "/ Orange In Bloom"
opus = "EATMD 13-01 19"
}}
\markuplist{ "Into..."
}

\score{{
\transpose d d' {
\time 3/4 \key g \major
  \repeat volta 2 {
  \partial 4 g8 a8
  b4 g4 e4 d4 g4 a4 b4 g4 e'4 d'2 g'8 fis'8
  e'4. fis'8 g'8 fis'8 e'4 d'4 b4
  } \alternative {
    {e'4 c'4 b4 a2 s4}
    {c'4 b4 a4 g2}
  }
  \bar "||" \break 
  \repeat volta 2 {
    b8 c'8
  d'4 b4 e'4 d'2 g8 a8 b4 g4 c'4 b2 g'8 fis'8
  \makeDoublePercent s1.
  } \alternative {
    { \makeDoublePercent s1.}
    { \makeDoublePercent s1 }
  }
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 20"
}}
\markuplist{ "Into..."
}

\score{{
\transpose d d' {
\time 3/4 \key g \major
  \repeat volta 2 {
  \partial 4 d4
  g4 g4 a4 b2 d'4 c'4. d'8 c'8 b8 a2 \grace {b8} c'4
  b4. c'8 b8 a8 g2 
  } \alternative {
    { b4 a4. b8 a8 g8 fis4 e4 }
    { fis4 g4 fis8 g8 a8 fis8 g2 }
  }
  \bar "||" \break
  \repeat volta 2 { d'4
  c'4. b8 a8 g8 fis2 c'4
  b4. a8 g8 fis8 e2 b4
  a4. g8 fis8 e8 fis4 g4 a4
  } \alternative {
    { b4. a8 g8 a8 b2 s4 }
    { g4 fis8 g8 a8 fis8 g2 }
  }
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 21"
}}

\score{{
\transpose d d' {
\time 2/2 \key g \major
  \partial 4. c'8 b8 a8 
  g4 g,4 g,4 b8 a8 b8 d'8 b8 g8 g8 fis8 e8 d8
  c4 e8 c8 b,4 d8 b,8 a,4 a4 a8 c'8 b8 a8
  \makePercent s1 \makePercent s1
  c'4 b8 a8 b4 a8 g8 d4 fis4 g8
  \bar "||" \break d'8 e'8 fis'8
  g'4 d'8 fis'8 e'8 c'8 b8 a8 b8 d'8 b8 g8 g8 fis8 e8 d8
  c4 e8 c8 b,4 d8 b,8 a,4 a4 a8 d'8 e'8 fis'8
  \makePercent s1 \makePercent s1
  c'4 b8 a8 b4 a8 g8 d4 fis4 g8
  \bar "|."  
}}
\header{
piece = "Sadler's Wells Hornpipe"
subtitle = "Hardcore 23-02"
opus = "EATMD 13-01 22"
}}

\markuplist{ "Into..."
}

\score{{
\transpose d d' {
\time 2/2 \key g \major
  \partial 4 b,8 a,8
  g,8 b,8 d8 b,8 g,8 b,8 d8 b,8 g,4 g4 g4 fis8 e8
  d8 fis8 a8 fis8 d8 fis8 a8 fis8 d4 d'4 d'4 b4 \noBreak
  c'8 d'8 e'8 c'8 b8 c'8 d'8 b8 a8 b8 c'8 d'8 e'8 fis'8 \afterGrace g'4 e'8
  g'8 d'8 e'8 c'8 d'8 b8 a8 g8 d4 g4 g4
  \bar "||" \break b8 c'8
  d'8 b8 g8 b8 d'8 b8 g8 b8 e'8 c'8 a8 c'8 e'8 c'8 a8 c'8
  g'8 fis'8 e'8 d'8 e'8 fis'8 g'8 a'8 fis'4 d'4 d'4 b4
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve
  \bar "|."  
}}
\header{
piece = "Butcher's Hornpipe"
subtitle = "Hardcore 14-03"
opus = "EATMD 13-01 23"
}}

\score{{
\transpose d d' {
\time 2/2 \key g \major
  g4 g4 \grace fis8 e4 d4 g4 g4 a4 g8 a8
  b4 b4 g8 a8 g8 a8 b8 a8 g8 a8 e4 d4
  \makePercent s1 \makePercent s1
  b4 b4 c'8 b8 a8 g8 e4 fis4 g2
  \bar "||" \break
  d'4 d'4 d'4 b8 d'8 e'4 d'4 \afterGrace d'2 {b8 d'8}
  e'4 d'4 b8 a8 g8 a8 b8 a8 g8 fis8 e4 d4
  \makeDoublePercent s\breve
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 24"
}}

\markuplist{ "Into (EATMD 13-01 25 = WFS 13-07 06) Getting Upstairs."
}

\score{{
\transpose d d' {
\time 2/2 \key d \major
  fis8 a8 d'8 e'8 fis'8 e'8 d'8 e'8 fis'8 e'8 d'8 cis'8 b4 a4
  g'8 fis'8 e'8 d'8 cis'8 a8 b8 cis'8 e'8 d'8 cis'8 b8 a2
  \makePercent s1 \makePercent s1
  \makePercent s1
  d'4 fis'4 d'2
  \bar "||" \break
  fis8 d8 fis8 a8 d'8 a8 fis8 d8 g4 fis8 d8 a,4 d4
  cis8 d8 e8 fis8 g8 e8 cis8 e8 d8 e8 fis8 g8 a2
  \makePercent s1 \makePercent s1
  \makePercent s1
  e4 d4 d2
  \bar "|."  
}}
\header{
piece = "Yarmouth Breakdown"
opus = "EATMD 13-01 26"
}}
\markuplist{ "Into..."
}

\score{{
\transpose d d' {
\time 4/4 \key d \major
  fis'8 e'8 d'8 b8 a4 fis4 g8 fis8 g8 a8 b2
  g'8 fis'8 e'8 d'8 cis'8 a8 b8 cis'8 e'8 d'8 cis'8 b8 a2
  \makePercent s1 \makePercent s1
  \makePercent s1
  d'4 fis'4 d'2
  \bar "||" \break
  fis4 a4 d'4. cis'8 b4 b4 e'4. fis'8
  g'8 fis'8 e'8 d'8 cis'8 a8 b8 cis'8 e'8 d'8 cis'8 b8 a2
  \makePercent s1 \makePercent s1
  \makePercent s1
  e'4 d'4 d'2
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 27"
}}

\score{{
\transpose d d' {
\time 6/8 \key d \major
  a8 b8 a8 a8 b8 a8 d'4 a8 a4 fis8
  a8 b8 a8 a8 b8 a8 e'4 a8 a4 fis8
  a8 b8 a8 a8 b8 a8 d'8 cis'8 d'8 e'4.
  fis'8 e'8 d'8 a8 b8 cis'8 d'4. d'4.
  \bar "||" \break
  fis'8 e'8 d'8 fis'8 e'8 d'8 e'4 a8 a4.
  fis'8 e'8 d'8 fis'8 e'8 d'8 g'4 e'8 e'4.
  fis'8 e'8 d'8 fis'8 e'8 d'8 g'8 fis'8 e'8 g'8 fis'8 e'8
  fis'8 e'8 d'8 a8 b8 cis'8 d'4. d'4.
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 28"
}}

\markuplist{ "Into (EATMD 13-01 29 = WFS 13-07 03) The Moon and Seven Stars."
}

\score{{
\transpose d d' {
\time 2/2 \key g \major
  \partial 4. d'8 e'8 fis'8
  g'4. a'8 g'8 fis'8 e'4 d'4. e'8 d'8 c'8 b8 a8
  g8 b8 d'8 b8 g8 b8 d'8 b8 c'4 b4 \afterGrace a2 {d'8 e'8 fis'8}
  \makePercent s1 \makePercent s1
  g8 b8 d'8 b8 c'8 a8 fis8 a8 a4 g4 g2
  \bar "||" \break
  \repeat volta 2 {
  g8 a8 b8 c'8 d'8 c'8 b8 a8 g8 a8 b8 c'8 d'4 b4
  c'4 a8 c'8 b4 g8 b8 a8 g8 fis8 e8 d2
  b4 b4 c'4 c'4 a4 a4 b4. a8
  g8 b8 d'8 b8 g8 b8 d'8 b8 c'4 b4 a2
  b4 b4 c'4 c'4 a4 a4 b4. a8
  g8 b8 d'8 b8 c'8 b8 a4
  } \alternative {
  {g2 g2} {g4 d'4 e'4 fis'4} }
  \bar "|."  
}}
\header{
piece = "Lodge Road"
subtitle = "Hardcore 42-01"
opus = "EATMD 13-01 30"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 2/2 \key g \major
  b4. b8 b4 b4 a8 g8 a8 b8 g4 a8 b8
  c'8 b8 a8 g8 g8 a8 b8 c'8 d'4 e'8 c'8 b4 a4
  \makePercent s1 \makePercent s1
  \makePercent s1 a2 g2
  \bar "||" \break
  g8 a8 b8 c'8 d'4. d'8 d'4 e'4 d'2
  e'4 d'4 g'4 d'4 d'4 e'8 c'8 b4 a4 \break
  b4. b8 b4 b4 a8 g8 a8 b8 g4 a8 b8
  c'8 b8 a8 g8 g8 a8 b8 c'8 d'4 e'8 c'8 b4 a4
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve
  \bar "|."  
}}
\header{
piece = "From Night Till Morn"
subtitle = "Welch MS; Sussex 05"
opus = "EATMD 13-01 31"
meter = "A(8) A B(4) A B A"
}}

\score{{
\transpose d d' {
\time 6/8 \key g \major
  \partial 4. d'8 c'8 a8
  g4 g8 e8 fis8 g8 a8 fis8 e8 d8 e8 fis8
  g8 a8 b8 c'8 d'8 e'8 d'8 b8 g8 d'8 c'8 a8
  \makePercent s2. \makePercent s2.
  g8 a8 b8 c'8 a8 fis8 g4.
  \bar "||" \break b8 c'8 d'8
  e'4 c'8 d'4 b8 c'4 a8 b8 c'8 d'8
  e'4 c'8 d'4 b8 c'4 b8 a4.
  \time 3/8
  d8 g8 fis8
  \time 6/8
  e4. c'8 b8 a8 fis4 d8 d8 e8 fis8
  g8 a8 b8 c'8 a8 fis8 g4.
  \bar "|."  
}}
\header{
piece = "South Downs"
composer = "Jim Harding"
opus = "EATMD 13-01 32"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 6/8 \key g \major
  \partial 8 d8
  g4 g8 a4 a8 b4 c'8 d'8 b8 g8
  e4 e8 c'4 b8 a4 g8 fis8 e8 d8
  \makePercent s2. \makePercent s2.
  e8 c'8 b8 a8 g8 fis8 g4. g4
  \bar "||" \break b8
  d'4 d'8 e'4 e'8 d'4 e'8 d'8 b8 g8
  d'4 d'8 e'4 e'8 d'8 b8 g8 a4.
  d'4 d'8 e'4 e'8 d'4 g'8 g'4 fis'8
  e'4 d'8 cis'8 b8 cis'8 d'4. d'4
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 33"
meter = "A A B A"
}}


\score{{
\transpose d d' {
\time 6/8 \key g \major
  d8 e8 fis8 g8 a8 b8 c'8 e'8 d'8 c'8 b8 a8
  b8 g8 e8 d8 d'8 c'8 b8 c'8 a8 g4.
  \bar "||" \break
  b8 c'8 d'8 d'4 d'8 e'4 e'8 d'8 b8 g8
  b8 c'8 d'8 \afterGrace e'4 fis'8 g'8 g8 a8 g8 fis8 e8 d8
  c'4 c'8 b8 d'8 b8 g8 fis8 g8 a8 fis8 d8
  g8 fis8 e8 d8 d'8 c'8 b8 c'8 a8 g4.
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 34"
meter = "A(4) A B(8) B"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 3/4 \key g \major
  \partial 4 d'4
  g'4 d'4 b4 g4. a8 b4
  c'4 e'4 a'8 g'8 fis'4. e'8 d'4
  g'4 d'4 b4 c'4. d'8 e'4
  d'4 g'4 fis'4 g'2
  \bar "||" \break a'4
  b'4 g'4 b'4 a'2 fis'4
  g'4 e'4 g'4 fis'4. g'8 a'4
  b'4 g'4 b'4 a'4 fis'4 d'4 g'4 fis'4 e'4 d'2
  \bar "|."  
}}
\header{
piece = "Sweet Jenny Jones"
subtitle = "/ Cadair Idris"
opus = "EATMD 13-01 35"
meter = "A A B A"
}}

\score{{
\transpose d d' {
\time 2/2 \key c \major
  \partial 4
  g4 c'4 c'4 b4 g4 c'4 c'4 d'4 d'4
  e'4 e'4 d'4 f'4 g'4. a'8 g'8 f'8 e'8 d'8
  c'4 c'4 b4 g4 c'4 c'4 d'4 d'4 e'4 g'4 f'4 e'4 e'2 d'2
  
  \bar "||" \break
  g'4 g'8 g'8 g'4 e'4 g'4 f'4 f'2
  e'4 e'4 d'4 d'4 c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8
  \makePercent s1 \makePercent s1
  e'4 e'4 d'4 d'4 c'8 e'8 g'8 e'8 c'2
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 36"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 2/2 \key c \major
  c'4 e'4 c'4 e'4 d'4 g'4 g'8 f'8 e'8 d'8
  c'4 e'4 c'4 e'4 d'8 c'8 b8 a8 g2
  \makePercent s1 \makePercent s1
  c'4 e'4 d'4 g'8 f'8 e'4 c'4 c'2
  \bar "||" \break
  d'8 cis'8 d'8 cis'8 d'4 f'4 e'4 c'4 c'4 e'4
  d'8 c'8 b8 a8 g4 b4 c'4 e'4 d'2
  \makePercent s1 \makePercent s1
  d'8 c'8 b8 a8 g8 a8 b4 c'4 e'4 c'2
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 37"
}}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  \partial 4 d4
  g8 b8 g8 a8 fis8 a8 d8 a8 g8 b8 g8 b8 d4 d4
  e4 e'4 e'8 d'8 c'8 b8 c'8 b8 a8 g8 g8 fis8 e8 d8
  \makePercent s1 \makePercent s1
  e8 e'8 d'8 c'8 b8 a8 g8 fis8 a4 g4 g4
  \bar "||" \break b8 c'8
  d'8 b8 d'8 b8 d'8 b8 d'8 b8 e'8 d'8 c'8 b8 c'4 a8 b8
  c'8 a8 c'8 a8 c'8 a8 c'8 a8 d'8 c'8 b8 a8 b4 d4
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 38"
}}
%}
\markuplist{ "Into (EATMD 13-01 39) abortive" }

\score{{
\transpose d d' {
\time 4/4 \key d \major
  d'8 a8 fis8 e8 d4. d'8
  <<
     {cis'8 a8 e8 cis8 d4 e8 fis8}
     \new Staff \ossia
     { \key g \major cis'8 a8 b8 cis'8 d'4 a8 fis8}
  >>
  g8 a8 b8 a8 g8 fis8 e8 d8 cis4 b,4 \afterGrace a,2
  {a8 b8 cis'8}
  \makePercent s1 \makePercent s2. e8 fis8
  g8 b8 a8 g8 fis8 e8 d8 cis8 e4 d4 d4
  \bar "||" \break a8 g8
  fis8 a8 d8 a8 fis8 a8 \afterGrace d4 a8
  g8 b8 e8 b8 g8 b8 \afterGrace e4 b8
  fis8 a8 d8 a8 fis8 a8 \afterGrace d4 a8
  cis8 e8 a,8 e8 cis8 e8 \afterGrace a,4 e8
  fis8 a8 d8 a8 fis8 a8 \afterGrace d4 a8
  g8 fis8 g8 a8 b8 cis'8 \times 2/3 {d'8 cis'8 b8}
  a8 d'8 cis'8 b8 a8 g8 fis8 e8 fis4 d4 d4	
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 40"
}}

\markuplist{
  "(EATMD 13-01 41) Mozart's Horn Concerto,
  into (EATMD 13-01 42) Trumpet Voluntary"
}



\score{{
\transpose d d' {
\time 2/2 \key c \major
  \partial 4 e8 f8 
  g4. a8 g4 e4 d2. e8 d8
  c4 e4 g4 a4 g2. c'4
  b4 a4 d4 e4 f2. b4
  a4 g4 c4 d4 e2. f4 \break 
  \makePercent s1 \makePercent s1
  c4 e4 g4 a4 b2 c'2
  d'4 b4 a8 g8 a8 b8 c'4 g4 g8 a8 g8 c'8
  b4 a4 f4 d4 c2 \bar "||" \break c4 d4 
  e4 c4 e4 c4 e2. c'4
  b4 a4 a4 g4 d2. c4
  b,4 c4 d4 e4 f2. g4
  b4 a4 g4 f4 e2. f4 \break
  \makePercent s1 \makePercent s1
  \makePercent s1 \makePercent s1
  b,4 c4 d4 e4 b2. a4
  g4 g4 a4 b4 c'2 \bar "||" \break e4 f4	
  g4. a8 g4 e4 d2. e8 d8
  c4 e4 g4 a4 g2. a8 b8
  c'4 b4 a4 g4 d2.
  g4 b4 g4 a4 g4 e2. d4
  e4 c4 g,4 a,8 b,8 c4 d8 e8 f4 d4
  e4 d4 a,4 b,4 c4 e4 g,2
  g,4 e4 e4 g,4 a,4 d4 f2
  e4 d4 a,4 b,4 c2 c4
  \bar "||" \break
  \bar "|."  
}}
\header{
piece = "Oscar Woods' March"
subtitle = "Hardcore 45-01"
opus = "EATMD 13-01 43"
meter = "A B C"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 2/2 \key c \major
  \partial 4 f4
  e2 e4 f4 g2. a4 g4 e'4 d'4 c'4 b2 a2
  d2 d4 e4 f2. g4 a4 b8 a8 g4 f4 e2. \break f4
  \makePercent s1 \makePercent s1
  \makePercent s1 \makePercent s1
  d'2 e'2 f'4 d'4 b4 a4 g4 g4 a4 b4 c'2.
  \bar "||" \break f4
  e4 g4 c'4. g8 e4 g4 c'4. g8 c'4 e'4 d'4 c'4 b2 a2
  b4 c'4 d'4. c'8 b4 c'4 d'4. c'8 b4 c'4 b4 a4 g2. \break f4
  \makePercent s1 \makePercent s1
  \makePercent s1 \makePercent s1
  d'2 e'2 f'4 d'4 b4 a4 g4 g4 a4 b4 c'2.
  \bar "|."  
}}
\header{
piece = "Oh Joe"
opus = "EATMD 13-01 44"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 2/2 \key c \major
  \partial 4 g,4
  c4 c4 d4 e4 g2. e4 f4 a4 b4 a4 g2. e4
  f4 f4 d4 f4 e4 e4 c4 e4 d4 a,4 b,4 c4 d4 b,4 a,4 g,4 \break
  \makePercent s1 \makePercent s1
  \makePercent s1 \makePercent s1
  \makePercent s1 \makePercent s1
  d4 a,4 b,4 g,4 c2
  \bar "||" \break c'4 b4 
  a1~a4 c'4 b4 a4 g2 e2~e4 g4 a4 g4
  g2 d2~d4 g4 a4 g4 g2 e2~e4 c'4 c'4 b4 \break
  \makePercent s1 \makePercent s1
  \makePercent s1 \makePercent s1
  \makePercent s1 \makePercent s2 d2~d4
  f4 e4 d4 c4. d8 e4 d4 c2.
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 45"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 2/2 \key c \major
  e4 g4 c4 e4 e4 d4 d2
  d4 f4 b,4 d4 d4 c4 c2
  \makePercent s1 \makePercent s1
  \makePercent s1 \makePercent s1
  \bar "||" \break
  e4 e4 d4 c4 b,4 d2 e4
  f4 f4 e4 d4 c4 e2 f4
  g2 c'4 b4 b4 a2.
  g4 g4 f4 d4 c2 c4 d4
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 46"
meter = "A B"
}}

\score{{
\transpose d d' {
\time 6/8 \key c \major
  \repeat volta 2 {
  \partial 4. g8 a8 b8
  c'4 e'8 d'4 c'8 b4. g8 a8 b8
  c'4 e'8 d'4 c'8 b4. g'4.
  f'4 e'8 d'4 c'8 b4 g8 a4 b8
  } \alternative {
    {  d'4 c'8 b4 a8 g4. s4. }
    {  c'4. e'4. c'2. }
  }
  \bar "||" \break
  e'4. g'4. e'4. g'4. a'4 g'8 f'4 e'8 d'2.
  f'4 e'8 d'4 c'8 b4 g8 a4 b8
  d'4 c'8 b4 a8 g4.  
  \bar "|."  
}}
\header{
piece = "George Green's Slow College Hornpipe"
subtitle = "Lester's 005"
opus = "EATMD 13-01 47"
meter = "A1 A2 B A2"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 6/8 \key g \major
  \repeat volta 2 {
  g4 fis8 g4 a8 b4 c'8 d'8 c'8 b8
  c'4 b8 c'4 d'8 e'4 fis'8 g'8 fis'8 e'8
  d'4 e'8 d'8 c'8 b8 \noBreak
  c'4 d'8 c'8 b8 a8
  } \alternative {
    {b4 c'8 b8 a8 g8 a8 b8 c'8 d'4.}
    {g4. b4. g4. b4 a8}
  }
  \bar "||" \break
  \repeat volta 2 {
  g8 b8 d'8 g'8 d'8 b8 g8 b8 d'8 g'4 fis'8
  e'4 fis'8 g'8 fis'8 e'8 d'4 c'8 b4.
  c'4 d'8 e'8 d'8 c'8 \noBreak
  } \alternative {
    {b4 c'8 d'8 b8 g8 
     a4. e'4. fis'4 e'8 d'8 c'8 a8}
    {b4. g4. a4. fis4. g2.}
  }
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 48"
}}


\score{{
\transpose d d' {
\time 6/8 \key g \major
  g'4 g'8 g4 a8 b4 c'8 d'4 e'8
  f'4 f'8 a4 b8 c'4 d'8 e'4 fis'8
  g'4 g'8 g4 a8 b4 c'8 d'4.
  e'8 fis'8 g'8 \afterGrace a'4 g'8 fis'8 g'4.
  \bar "||" \break d''4 c''8
  b'8 c''8 b'8 g'8 a'8 b'8 c''4 b'8 a'4 g'8
  fis'4 e'8 d'4 e'8 fis'4 g'8 a'4 c''8
  \makePercent s2. \makePercent s2.
  \afterGrace fis'4 e'8 d'8 e'4 fis'8 g'4.
  \bar "|."  
}}
\header{
piece = "The Fiery Clock Face"
opus = "EATMD 13-01 49"
}}

\score{{
\transpose d d' {
\time 4/4 \key c \major
  c'4 c'4 c'4 g8 e8 f4 f8 e8 d2
  b,8 c8 d8 e8 f8 e8 f8 d8 c8 d8 e8 f8
  g8 a8 b8 g8
  \makePercent s1 \makePercent s1
  b,8 c8 d8 e8 g8 f8 e8 d8 c4 e4 c4
  \bar "||" \break g8 f8
  \times 2/3 {e8 g8 e8} c4
  \times 2/3 {e8 g8 e8} c4 d8 e8 f8 e8 d2
  \times 2/3 {d8 f8 d8} b,4
  \times 2/3 {d8 f8 d8} b,4 c8 d8 e8 f8 g2
  \makePercent s1 \makePercent s1
  b,8 c8 d8 e8 g8 f8 e8 d8 c4 e4 c4  
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 50"
}}

\markuplist{ "Into (EATMD 13-01 51 = EATMD 13-01 26) (in C)"
}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  \partial 4 g8 a8
  b4 g4 d4 g8 a8 b4 g4 d4 \times 2/3 {g8 a8 b}
  c'4 a4 fis4 d4 c'4 a4 fis4 d4
  \makePercent s1 \makePercent s2. g4
  fis8 g8 a8 b8 c'8 d'8 e'8 fis'8 g'2.
  \bar "||" \break d'4
  b'4 a'4 g'4 fis'4 g'8 fis'8 g'8 fis'8 g'4
  b8 c'8 d'4 a8 b8 c'4 a4 g8 a8 b8 c'8 d'4 d'4
  \makePercent s1 \makePercent s1
  d'4 a8 b8 c'8 a8 fis8 a8 g4 b4 g4
  \bar "|."  
}}
\header{
piece = "Walter Bulwer's Polka #4"
subtitle = "Hardcore 54-02"
opus = "EATMD 13-01 52"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 4/4 \key g \major
  b4 b4 b8 a8 g8 a8 b4 d4 d2
  e4 g4 g4 a4 g2. d4
  d4 g4 a4 b4 d'4 b2 a4 g4 e4 fis4 g4 a2. g8 a8
  \makePercent s1 \makePercent s1
  \makePercent s1 \makePercent s1
  b4 b4 c'4 b4 a4 e2 g4 fis4 d4 b4 a4 g2
  \bar "||" \break d'4. c'8
  b4 b4 d'4 b8 a8 g4 g4 b4 g8 fis8
  e4 e4 fis4 g4 c'2. b4
  c'4 e'4 a4. b8 c'4 e'4 a4. g8
  fis4 g4 fis4 e4 d2. d'4
  e'4 d'4 b4 g4 d2. g4 fis4 g4 a4 b4 c'1
  d'4 c'4 a4 fis4 d'4 c'4 a4 fis4
  d4 d4 e4 fis4 g1
  \bar "|."  
}}
\header{
piece = "Walter Bulwer's Polka #3"
subtitle = "Hardcore 54-01"
opus = "EATMD 13-01 53"
meter = "A B"
}}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  g4 g4 g4 fis8 g8 a4 a4 a2
  g8 fis8 e8 d8 e4 fis4 g8 a8 b8 c'8 d'8 c'8 b8 a8  
  \makePercent s1 \makePercent s1
  g2
  \bar "||" \break g4 a4
  b4 b4 b4 a8 b8 c'4 c'4 c'2
  a4 a4 a4 g8 a8 b4 b4 b8 c'8 d'8 b8
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 54"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 6/8 \key g \major
  g8 fis g8 g4 b8 g8 fis8 g8 g4 b8
  a8 fis8 d8 d4 b8 a8 fis8 d8 d4.
  \makePercent s2. \makePercent s2.
  a8 fis8 d8 d8 e8 fis8 g4. g4.
  \bar "||" \break
  d'4 b8 d'4 b8 g4 g8 g4.
  e'4 c'8 e'4 c'8 a4 a8 a8 b8 c'8
  \makePercent s2. \makePercent s2.
  a4 a8 d8 e8 fis8 g4. g4.
  \bar "|."  
}}
\header{
piece = "The New-Rigged Ship"
opus = "EATMD 13-01 55"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 6/8 \key g \major
  \partial 8 d8
  g4 d8 g4 d8 g4 d8 g4 b8
  d'8 c'8 b8 b8 a8 g8 a4. a4 d8
  \makePercent s2. \makePercent s2.
  d'8 c'8 b8 a8 g8 a8 g4. g4
  \bar "||" \break d8
  b8 a8 b8 c'8 b8 c'8 d'4. b4 c'8
  d'8 c'8 b8 b8 a8 g8 a4. a4 d8
  \makePercent s2. \makePercent s2.
  d'8 c'8 b8 a8 g8 a8 g4. g4
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 56"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 6/8 \key g \major
  d8 e8 d8 d8 e8 d8 b4 g8 a4 b8 
  c'4 a8 fis4 a8 d'4 b8 g8 fis8 e8
  \makePercent s2. \makePercent s4.~s4
  c'8 b8 c'8 d'8 c'8 b8 a8 g4. g4.
  \bar "||" \break
  b4. d'4. e'4 d'8 b4 g8
  a8 b8 a8 e4 fis8 a4 g8 d4.
  \makePercent s2. \makePercent s2.
  \makePercent s2. g2.
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 57"
}}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  g4 g4 g4 g4 fis8 g8 a8 fis8 g4. a8
  b4 b4 b4 b4 a8 b8 c'8 a8 b2
  \bar "||" \break
  \repeat volta 2 {
  c'8 d'8 e'8 c'8 a4 a4 b8 c'8 d'8 b8 g4 g4
  a8 b8 c'8 a8 fis8 d8 e8 fis8
  } \alternative {
    {g8 a8 b8 c'8 d'2}
    {g4 b4 g2}
  }
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 58"
meter = "A B B"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 4/4 \key g \major
  d8 e8 d8 g8 b4 b4 d8 e8 d8 g8 b4 b4
  c'8 b8 a8 g8 fis8 d8 e8 fis8 a8 g8 fis8 e8 d2
  \makePercent s1 \makePercent s1
  \makePercent s1 g4 b4 g4
  \bar "||" \break b8 c'8
  d'4 c'4 b4 a4 g8 a8 b8 g8 e2
  c'4 b4 a4 g4 fis8 g8 a8 fis8 d2
  \makePercent s1 \makePercent s1
  c'8 b8 a8 g8 fis8 d8 e8 fis8 g4 b4 g4
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-01 59"
}}


%{ Outside session recording. %}


\score{{
\transpose d d' {
\time 6/8 \key g \major
  \partial 4. b4 c'8
  d'8 b8 g8 c'8 a8 fis8 g8 b8 d'8 g'4 fis'8
  e'8 d'8 c'8 b8 a8 g8 fis8 g8 a8 a8 b8 c'8
  \makePercent s2. \makePercent s4. g'4 b'8
  a'8 g'8 fis'8 e'8 d'8 cis'8 d'4.
  \bar "||" \break fis'4 g'8
  a'8 fis'8 d'8 d'8 fis'8 g'8 a'8 fis'8 d'8 d'4 b8
  c'8 e'8 c'8 b8 d'8 b8 c'8 a8 a8 a8 b8 c'8
  d'8 b8 d'8 e'8 c'8 e'8 fis'8 e'8 fis'8 g'8 fis'8 e'8
  d'8 c'8 b8 a8 g8 fis8 g4.
  \bar "|."  
}}
\header{
piece = "Juniper Hill"
subtitle = "Hardcore 60-02"
opus = "EATMD 13-02 01"
}}


\score{{
\transpose d d' {
\time 3/2 \key g \major
  
  b4. c'8 d'4 b4 a4 g4 fis4 a2 c'4 b4 a4
  b4. c'8 d'4 b4 a4 g4 d4 g2
  \bar "||" b4 a4 g4 \break 
  b4. c'8 d'4 e'4 fis'4 g'4 a'4 a2 c'4 b4 a4
  b4. c'8 d'4 e'4 fis'4 g'4 g'4 g2
  \bar "|." b4 a4 g4
}}
\header{
piece = "The Dusty Miller"
opus = "EATMD 13-02 02"
}}
\markuplist{ "Into..."
}

\score{{
\transpose d d' {
\time 3/2 \key g \major
  g8 a8 b8 c'8 d'4 g4 b4 g4 fis4 a4 a4 c'4 b4 a4
  g8 a8 b8 c'8 d'4 g4 b4 g4 d4 g4 g4
  \bar "||" b4 a4 g4 \break 
  g'2 fis'2 e'2 fis'4 d'2 fis'4 e'4 d'4
  c'2 b2 a2 b4 g2 
  \bar "|." b4 a4 g4 
}}
\header{
piece = "Punchinello's Hornpipe"
subtitle = "/ The Three Rusty Swords"
opus = "EATMD 13-02 03"
}}
\markuplist{ "Into..."
}

\score{{
\transpose d d' {
\time 3/2 \key d \major
  fis4. e8 d4 fis'4 e'4 d'4 e'4 e2 b4 a4 g4
  fis4. e8 d4 fis'4 e'4 d'8 cis'8 d'4 d2
  \bar "||" b4 a4 g4 \break 
  fis4 a4 g4 b4 a4 cis'8 d'8 e'4 e2 b4 a4 g4
  fis4 a4 g4 b4 a4 b8 cis'8 d'4 d2
  \bar "||" fis'4 g'4 a'4 \break 
  fis'4. e'8 d'4 fis'4 e'4 d'4 cis'4 e'2 fis'4 g'4 a'4
  fis'4. e'8 d'4 fis'4 e'4 cis'4 d'4 d2
  \bar "|." b4 a4 g4 
}}
\header{
piece = "Old Lancashire Hornpipe"
meter = "A A B B C C"
opus = "EATMD 13-02 04"
}}


\score{{
\transpose d d' {
\time 4/4 \key g \major
  \partial 4 d'8 c'8
  b4 a4 g4 d'8 c'8 b4 a4 g4 d'4
  e'4. d'8 c'8 d'8 e'4 d'4. c'8 b8 c'8 d'4
  c'4 b4 a4 g4 fis8 g8 a8 fis8 d4 d'8 c'8
  b8 a8 g8 b8 a4 fis4 g2.
  \bar "||" \break d'4
  e'4. d'8 e'4. d'8 e'4 fis'4 g'4. fis'8
  g'4 fis'4 e'4 d'4 b8 a8 g8 b8 a4 d4
  g4 g4 a4 a4 \afterGrace b4 a8 g4 g'4. fis'8
  g'4 d'4 e'2 d'4 b4 c'2
  c'4 b4 a4 g4 fis8 g8 a8 fis8 d4 d'8 c'8
  b8 a8 g8 b8 a4 fis4 g2.
  \bar "|."  
}}
\header{
piece = "The Princess Royal"
meter = "A(8) A B(12)"
opus = "EATMD 13-02 05"
}}

\score{{
\transpose d d' {
\time 6/8 \key g \major
  g'4. g4 a8 b8 d'8 c'8 b8 a8 g8
  g'4. g4 a8 e8 a8 g8 fis8 e8 d8
  \makePercent s2. \makePercent s2.
  e8 fis8 g8 a8 b8 c'8 b8 g8 g8 g4.
  \bar "||" \break
  b8 g8 b8 d'8 b8 d'8 e'8 fis'8 g'8 d'8 b8 g8
  b8 g8 b8 d'8 b8 g8 fis8 g8 a8 a4 c'8
  \makePercent s2. \makePercent s2.
  e8 fis8 g8 a8 b8 c'8 b8 g8 g8 g4.
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-02 06"
}}

\markuplist{ "Into..." }

\score{{
\transpose d d' {
\time 6/8 \key g \major
  g'4 g8 g8 fis8 g8 e8 g8 g8 d8 g8 g8
  g'4 g8 g8 fis8 g8 e8 a8 g8 fis8 e8 d8
  \makePercent s2. \makePercent s2.
  e8 g8 g8 fis8 g8 a8 b8 g8 g8 g4.
  \bar "||" \break
  \repeat volta 2 {
  g8 b8 d'8 d'8 b8 g8 g8 b8 d'8 d'4 a8
  g8 b8 d'8 d'8 c'8 b8 c'8 b8 c'8 a4 a8
  \makePercent s2. \makePercent s4. d'8 e'8 fis'8
  g'8 fis'8 e'8 d'8 c'8 b8
  } \alternative {
    { a8 g8 fis8 g4. }
    { a8 b8 c'8 d'8 e'8 fis'8 }
  }
  \bar "|."  
}}
\header{
piece = "?"
opus = "EATMD 13-02 07"
}}

\markuplist{ "? (EATMD 13-02 08 = WFS 13-07 18) into..." }

\score{{
\transpose d d' {
\time 4/4 \key g \major
  g4 d'4 b2 a8 b8 a8 g8 <fis e>4 d4
  g4 d'4 b2 d'4 c'8 b8 a2
  \makePercent s1 \makePercent s1
  e4 e4 c'4 b8 a8 <fis g>4 fis4 g2
  \bar "||" \break
  fis4. g8 a4 b4 c'4 b4 a2
  g4 e4 c'4 d'4 b2 a2
  d'8 e'8 d'8 c'8 b4 b4 g4 g4 e2
  c'4 b8 a8 g4 fis8 g8 a2 g2
  \bar "|."  
}}
\header{
piece = "Mount Hills"
subtitle = "Lester's 349; Hardcore 43-03"
opus = "EATMD 13-02 09"
}}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  b8 c'8 d'8 b8 c'4 c'4 b8 c'8 d'8 b8 a2
  b8 c'8 d'8 b8 c'4 b8 c'8 d'4 d4 g2
  \bar "||"
  b4 g4 c'2 b4 g4 a2
  \makeDoublePercent s\breve
  \bar "|."  
}}
\header{
piece = "Shepherds' Hey"
opus = "EATMD 13-02 10"
}}

\markuplist{ "Jenny Lind Polka (EATMD 13-02 11 = WFS 13-07 04) into..." }

\score{{
\transpose d d' {
\time 4/4 \key g \major
  \partial 4 g'8 fis'8
  e'4 d'8 c'8 b4 a4 b4 g4 e4 d4
  g4 g4 g8 a8 b8 c'8
  \afterGrace d'2 { e'8 d'8 c'8 } b4 g'8 fis'8
  \makePercent s1 \makePercent s1
  fis8 g8 a4 d4 e8 fis8 g2 g4
  \bar "||" \break d'8 c'8
  b4 d'4 e'4 fis'4 
  <<
    { g'4 d'4 b4 d'8 c'8 }
     \new Staff \ossia
    { \key g \major g'4 d'8 c'8 b8 a8 \afterGrace g4 a8 }
  >>
  \afterGrace b4 c'8 d'4 e'4 fis'4 g'2 fis'4 g'8 fis'8
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve
  \bar "|."  
}}
\header{
piece = "Brighton Camp"
opus = "EATMD 13-02 12"
}}

\score{{
\transpose d d' {
\time 4/4 \key d \major
  fis4 fis4 d8 fis8 a8 d'8 d'8 a8 fis8 d8 e2
  d8 fis8 a8 d'8 d'8 cis'8 d'8 fis'8 e'8 d'8 cis'8 b8 \afterGrace a2 {g8 fis8 e8}
  \makePercent s1 \makePercent s1
  d8 fis8 a8 d'8 cis'8 d'8 e'8 cis'8 d'4 d'4 d'2
  \bar "||" \break
  a8 cis'8 e'8 fis'8 g'8 fis'8 g'8 e'8 d'8 e'8 fis'8 g'8 \afterGrace a'2 {fis'8 a'8}
  \afterGrace g'2 {e'8 g'8} \afterGrace fis'2 {d'8 fis'8} e'8 d'8 cis'8 b8 a8 g8 fis8 e8
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve
  \bar "|."  
}}
\header{
piece = "Coleford Jig"
opus = "EATMD 13-02 13"
}}

%{
\score{{
\transpose d d' {
\time 6/8 \key g \major
  \makePercent s2. \makePercent s2.
  \bar "||" \break
  \bar "|."  
}}
\header{
piece = "?"
}}
\markuplist{
}
%}

