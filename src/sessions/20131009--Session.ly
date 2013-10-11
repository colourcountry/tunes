\version "2.16.0"

\layout { 
  indent = 0.0\cm
  \context { \Score \remove "Bar_number_engraver" }	
  \context { \Staff \remove "Time_signature_engraver" }
}

#(set-global-staff-size 18)

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


  
%{
\score{{
\transpose d d' {
\time 4/4 \key g \major
  \partial 4 g8 a8
  b4 b4 b4 b4 b4 d'2 b4
  b4 a4 a4 b4 a2. d'4
  e'4 c'4 g'4. fis'8 e'4 d'4 b4 g4
  a4 g4 g4 a4 g2
  \bar "||" \break g'4. fis'8
  e'4 d'4 b4 c'4 d'2 g'4. fis'8
  e'4 d'4 g4 a4 b2. s4
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve
  \bar "|."
}}
\header{
piece = "?"
opus = "WFS 13-10 01"
}}

\markuplist{ "Brighton Camp (WFS 13-10 02 = EATMD 13-02 12)" }

\score{{
\transpose d d' {
\time 4/4 \key g \major
  b4 d'4 d'4 b4 c'4 e'4 e'4 c'4
  b4 d'4 d'4 b4 c'4 a4 a2
  \makePercent s1 \makePercent s1
  b4 d'4 a4. c'8 b4 g4 g2
  \bar "||" \break
  b4 d'4 d'4 e'8 fis'8 g'8 fis'8 g'8 fis'8 g'4 d'4
  b4 d'4 d'4 b4 \afterGrace c'4 b8 \afterGrace a4 <b g>8 a2
  \makePercent s1 \makePercent s1
  b4 d'4 a4. c'8 b4 g4 g2
  \bar "|."
}}
\header{
piece = "?"
opus = "WFS 13-10 03"
}}

\markuplist{ "Uncle Bernard's Polka (WFS 13-10 04 = WFTB 02-01) into Jamie Allen (WFS 13-10 05 = WFTB 02-03)" }

\score{{
\transpose d d' {
\time 6/8 \key d \major
  \partial 8 a8
  d'4 d'8 \afterGrace d'4 cis'8 b8 \afterGrace a4. g8 fis4 a8
  d'4 d'8 e'4 cis'8 d'4.~d'4 a8
  d'4 e'8 fis'4 g'8 a'4 fis'8 d'4 e'8
  fis'4 fis'8 fis'8 e'8 d'8 e'4.~e'4 a8
  d'4 e'8 fis'4 g'8 a'4 fis'8 d'4 e'8
  fis'4 fis'8 fis'8 e'8 d'8 e'4. fis'4 e'8
  d'4 d'8 d'8 cis'8 b8 a4 g8 \afterGrace fis4 a8 a8
  d'4 d'8 e'4 cis'8 d'4.~d'4
  \bar "|."
}}
\header{
piece = "The Lincolnshire Poacher"
opus = "WFS 13-10 06"
}}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  b4 g8 b8 c'4 a8 c'8 b4 g8 b8 a8 fis8 d4
  b4 g8 b8 c'4 a8 c'8 b8 g8 a8 fis8 g2
  \bar "||" \break
  b8 d'8 d'8 g'8 e'4 d'8 c'8 b4 g8 b8 a8 fis8 d4
  b8 d'8 d'8 g'8 e'4 d'8 c'8 b8 g8 a8 fis8 g2
  \bar "|."
}}
\header{
piece = "?"
opus = "WFS 13-10 07"
}}
\markuplist{"Into..."
}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  d'4 d'8 c'8 b8 c'8 d'4
  a8 b8 c'8 b8 a8 b8 c'4
  d'4 d'8 c'8 b8 c'8 d'4
  g8 a8 \afterGrace b4 g8 a4 g4
  \bar "||" \break
  b8 g8 d8 g8 b8 g8 b4
  c'8 a8 fis8 a8 c'8 a8 c'4
  b8 g8 d8 g8 b8 g8 b4
  g8 a8 \afterGrace b4 g8 a4 g4
  \bar "|."
}}
\header{
piece = "?"
opus = "WFS 13-10 08"
}}
\markuplist{
}

\score{{
\transpose d d' {
\time 4/4 \key e \minor
  b4 e4 e2 b4 e4 e4. fis8 g4 g4 fis4 g4 a2 g4 a4
  b4 b4 a4 a4 g4 g4 fis2 e8 fis8 g4 fis4 d4 e1
  \bar "||" \break
  e8 fis8 g4 e8 fis8 g4 fis4 d4 d2 e8 fis8 g4 e8 fis8 g4 a2 g4 a4
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve
  \bar "|."
}}
\header{
piece = "Bear Dance"
opus = "WFS 13-10 09 = WFTB 02-01"
}}

\markuplist{ "Horses Brawl (WFS 13-10 10 = WFS 13-07 09)" }

\markuplist{ "Oscar Woods' Jig (WFS 13-10 11 = WFS 13-07 01) into Captain Lanoe's Quick March (WFS 13-10 12 = WFS 13-07 02)" }

\score{{
\transpose d d' {
\time 6/8 \key g \major
  b4 b8 b8 c'8 d'8 e'4 e'8 e'4.
  d'4 d'8 d'4 e'8 d'4 c'8 b4 a8
  \makePercent s2. \makePercent s2.
  d'8 e'8 fis'8 g'8 d'8 b8 a4. g4.
  \bar "||" \break
  g'4. fis'4. e'4. d'8 e'8 fis'8
  \afterGrace g'4. g'8 \afterGrace fis'4. fis'8
  \afterGrace e'4. e'8 d'4 c'8
  \makeDoublePercent s1.
  \makeDoublePercent s1.
}}
\header{
piece = "Rogue's March"
opus = "WFS 13-10 12"
}}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  g4 e4 d4 e4 g2 g4 a4 b4 d'4 a4 b8 a8 g4 e4 d2
  \makePercent s1 \makePercent s1
  b4 d'4 a4 b8 a8 g2.
  \bar "||" \break 
  \repeat volta 2 {
  a4
  b4 d'4 \afterGrace d'2 {c'8 b8} c'4 e'4 e'2
  d'4 b4 a4 b8 a8 g4 e4 d2}
  \alternative {
  { \makePercent s1 \makePercent s2.~s8 fis'8
  g'4 fis'4 e'4 d'4 e'4 fis'4 g'2 }
  { \makeDoublePercent s\breve
  \makeDoublePercent s\breve }
  }
  \bar "|."
}}
\header{
piece = "Salmon Tails Up The Water"
opus = "WFS 13-10 13 = WFTB 01-02"
}}
\markuplist{"Into..."
}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  g4 b4 g4 b4 \afterGrace g4 a8 \afterGrace b4 c'8 d'2
  a4. c'8 b4 a4 g4 b4 d'2
  c'4 e'4 fis'4 e'4 d'4 b4 d'2
  a4. c'8 b4 a4 g2 g2
  \bar "||" \break 
  g'4 fis'4 e'4 d'4 g'4 fis'4 e'4 d'4
  g'4 fis'4 e'4 d'4 c'4 b4 a2
  fis'4 e'4 d'2 fis'4 e'4 d'2
  d'2 a4. c'8 b4 a4 g2
  \bar "|."
}}
\header{
piece = "Winster Gallop"
opus = "WFS 13-10 14 = WFTB 01-01"
}}

\markuplist{"Into Rakes of Mallow (WFS 13-10 15 = WFTB 01-03)"
}

\score{{
\transpose d d' {
\time 4/4 \key d \major
  a4 fis8 a4 d8 fis8 a8 b4 g8 b4 d8 g8 b8
  a4 fis8 a4 d8 fis8 a8 e8 fis8 g8 a8 g8 fis8 e8 d8
  \makePercent s1 \makePercent s1
  a8 b8 cis'8 d'8 e'8 fis'8 g'8 e'8 fis'4 d'4 d'4
  \bar "||" \break e'4
  fis'4 d'8 fis'4 a8 d'8 fis'8 g'8 e'8 a'8 fis'8 g'8 fis'8 e'8 d'8
  fis'4 d'8 fis'4 a8 d'8 fis'8 e'4 cis'8 e'4 a8 cis'8 e'8
  \makePercent s1 \makePercent s1
  a8 b8 cis'8 d'8 e'8 fis'8 g'8 e'8 fis'4 d'4 d'4
  \bar "|."
}}
\header{
piece = "Willafjord"
opus = "WFS 13-10 16"
}}

\markuplist{"Donkey Riding (WFS 13-10 17 = WFTB 04-03) into Bobby Shaftoe (WFS 13-10 18 = WFTB 04-04)"
}
\markuplist{"(Break)"
}
\markuplist{"La Roulante (WFS 13-10 19 = WFS 13-07 15)"
}

\score{{
\transpose d d' {
\time 6/8 \key e \minor
  \afterGrace e4 d8 e8 g4 a8 b4 a8 b8 cis'8 d'8
  \afterGrace d4 e8 d8 fis4 g8 a8 b8 a8 fis8 e8 d8
  \makePercent s2. \makePercent s2.
  e'4 b8 c'8 b8 a8 b8 g8 e8 e4.
  \bar "||" \break
  e'4 fis'8 g'8 fis'8 e'8 fis'8 a'8 g'8 fis'8 e'8 d'8
  e'4 fis'8 g'8 fis'8 e'8 fis'8 b8 b8 b4.
  \makePercent s2. \makePercent s2.
  e'4 b8 c'8 b8 a8 b8 g8 e8 e4.
  \bar "|."
}}
\header{
piece = "Lannigan's Ball"
opus = "WFS 13-10 20"
}}

\score{{
\transpose d d' {
\time 4/4 \key d \major
  \partial 4 a8 g8
  fis4 a4 d4 a8 g8 fis4 a4 d4 d'4
  cis'4 d'4 e'4 cis'4 d'8 cis'8 d'8 e'8 fis'4 a8 g8
  \makePercent s1 \makePercent s2. d'4
  cis'4 d'4 e'4 cis'4 d'2.
  \bar "||" \break e'4
  fis'4 \afterGrace d'4 d'8 d'4 fis'4 g'4 \afterGrace e'4 e'8 e'4 g'4
  fis'4 \afterGrace d'4 d'8 d'4 fis'4 e'8 d'8 cis'8 b8 a4 e'4
  \makePercent s1 \makePercent s2. g'4
  fis'4 d'4 e'4 cis'4 d'2.
  \bar "|."  
}}
\header{
piece = "Harper's Frolic"
opus = "WFS 13-10 21"
}}
\markuplist{"Into..."
}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  
  g'4. fis'8 g'4. fis'8 g'4 d'4 d'4 b4
  c'8 d'8 e'4 d'4 c'4 b4 g4 g4 a4
  b4 g4 g4 a8 b8 c'4 a4 a4 c'4
  b8 c'8 d'4 c'4 b4 \afterGrace a1 {d'4 e'4 fis'4}
  \bar "||" \break
  b4 g4 g4 a8 b8 c'4 a4 d'4 b4
  e'4 c'4 c'4 d'8 e'8 fis'4 d'4 d'4 e'8 fis'8
  g'4. fis'8 g'8 fis'8 e'4 d'4 e'8 fis'8 g'4 b4
  c'8 d'8 e'4 d'4 c'4
  b4 g4 \afterGrace g2 a4
  \bar "|."  
}}
\header{
piece = "Bonnie Kate"
opus = "WFS 13-10 22"
}}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  \partial 4 d'8 c'8
  b4 g4 g4 a8 b8 c'8 b8 a8 g8 fis4 d4
  g4 b4 g4 b4 g8 a8 b8 c'8 d'4 d'8 c'8
  \makePercent s1 \makePercent s1
  g4 b4 a4 d'8 c'8 b4 g4 g4
  \bar "||" \break b8 c'8
  d'4. e'8 d'4. e'8 d'8 c'8 b8 a8 g2
  a4 a8 b8 c'8 b8 c'8 d'8 e'4 a4 a4 b8 c'8
  \makePercent s1 \makePercent s1
  a4 a4 d4 e8 fis8 g2 g4
  \bar "|."  
}}
\header{
piece = "The Bonny Breast Knot"
opus = "WFS 13-10 23"
}}
%}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  g8 a8 b8 c'8 d'4 d'4 c'4 e'4 a4 b8 c'8
  d'4 d'4 e'4 d'8 c'8 b4 a4 g2
  \makePercent s1 \makePercent s1
  \makePercent s1 \makePercent s1
  \bar "||" \break
  e4 d4 e8 fis8 g4 a4 a4 g4. a8
  b4 a4 b8 c'8 d'4 e'4 e'4 d'8 c'8 b8 a8
  \makeDoublePercent s\breve
  \makeDoublePercent s\breve
  \bar "|."  
}}
\header{
piece = "Young Collins"
opus = "WFS 13-10 24"
}}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  \partial 4 d8 e8
  g4 d8 e8 g8 d8 e8 g8 d8 e8 g8 a8 b4 a8 b8
  g4 d8 e8 g8 a8 b8 d'8 e'8 g'8 e'8 d'8 b4 a8 b8
  \makePercent s1 \makePercent s1
  g'4 e'8 d'8 e'8 d'8 b8 a8 b4 g4 g4 
  \bar "||" \break e'8 fis'8
  g'4 e'8 d'8 e'8 d'8 b4 b8 a8 b8 g8 e4 d8 e8
  g8 a8 b8 d'8 e'8 g'8 e'8 d'8 b4 a4 a4 e'8 fis'8
  \makePercent s1 \makePercent s1
  g8 a8 b8 d'8 e'8 g'8 e'8 d'8 b4 g4 g4
  \bar "|."  
}}
\header{
piece = "Spootiskerry"
opus = "WFS 13-10 25"
meter = "A B B"
}}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  \partial 4 b8 a8
  g8 b8 d'4 d'4 c'8 b8 a8 c'8 e'4 e'4 d'8 c'8
  b8 d'8 g'8 d'8 c'8 e'8 d'8 c'8 b4 g4 g4 b8 a8
  \makePercent s1 \makePercent s1
  \makePercent s1 \makePercent s2.
  \bar "||" \break b8 d'8
  g'4 g'8 fis'8 g'8 d'8 b8 d'8 e'4 d'4 d'4 e'8 fis'8
  g'8 d'8 g'8 fis'8 g'8 d'8 b8 d'8 c'4 a4 a4 e'8 fis'8
  \makeDoublePercent s\breve
  \makeDoublePercent s1~s2.
  \bar "|."  
}}
\header{
piece = "?"
opus = "WFS 13-10 26"
}}

\score{{
\transpose d d' {
\time 4/4 \key d \major
  \partial 4 a4
  d'4 a8 g8 fis8 d8 fis8 a8 b8 g8 b8 d'8 cis'8 a8 cis'8 e'8
  fis'4 fis'4 g'8 fis'8 e'8 d'8 cis'4 e'4 e'4 a4
  \makePercent s1 \makePercent s1
  fis'4 fis'4 g'8 fis'8 e'8 d'8 a4 d'4 d'4
  \bar "||" \break a4
  d'8 fis'8 a'8 fis'8 d'8 fis'8 a'8 fis'8 g'8 fis'8 e'8 fis'8 g'4 e'8 fis'8
  g'8 fis'8 e'8 d'8 cis'8 d'8 e'8 g'8 fis'8 e'8 fis'8 g'8 <fis' a'>4 fis'8 e'8
  \makePercent s1 \makePercent s1
  g'8 fis'8 e'8 d'8 cis'8 <a a'>8 a'8 g'8 fis'4 d'4 d'4
  \bar "|."  
}}
\header{
piece = "?"
opus = ""
}}

%{
\score{{
\transpose d d' {
\time 6/8 \key g \major
  \bar "||" \break 
  \bar "|."  
}}
\header{
piece = "?"
opus = ""
}}
\markuplist{
}
%}

