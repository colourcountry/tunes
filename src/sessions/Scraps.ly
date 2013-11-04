\version "2.16.0"
\layout { indent = 0.0\cm }

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
piece = "Monsal Head"
}}

\score{{
\transpose d d' {
\time 4/4 \key g \major
  \partial 4. d'8 e'8 fis'8
  g'8 b8 d'8 e'8 g8 b8 d'8 e'8
  d'8 c'8 a8 fis8 d8 e8 fis8 g8
  a8 b8 c'8 d'8 ees'8 e'8 f'8 fis'8
  e'8 d'8 b8 g8 d8 d'8 e'8 fis'8
  \makePercent s1 \makePercent s1
  \makePercent s1 g'8 d'8 b8 g4
  \bar "||" \break
  g'8 fis'8 g'8
  e'8 c'8 c''8 e'8 a'8 g'8 e'8 c'8
  b8 g8 g'8 b8 e'8 d'8 b8 g8
  a8 b8 c'8 d'8 ees'8 e'8 f'8 fis'8
  e'8 d'8 b8 g8 d8 g'8 fis'8 g'8
  \makePercent s1 \makePercent s1
  \makePercent s1 g'8 d'8 b8 g4
  \bar "|."
}}
\header{
piece = "?"
}}

\score{{
\transpose d g' {
\time 9/8 \key g \major
  d4. g4. a4 b8 c'4 b4 g4 e4.~e4.
  c'4 b8 a4 g8 fis8 g8 a4 fis4 d4.
  \makePercent s2.~s4. \makePercent s2.~s2.
  c'4 b8 a4 g8 fis8 e8 fis8 g2.
  \bar "||" \break
  g4 b8 d'4 c'8 b4 a8 g8 c'8 e'4 d'4 c'4 b8
  a4 b8 \times 3/4 {c'8 d'8 c'8 a8} b4 g8
  fis8 g8 a4 fis4 d4.
  \makePercent s2.~s4. \makePercent s2.~s4.
  a4 b8 \times 3/4 {c'8 d'8 c'8 a8} b4 g8
  fis8 e8 fis8 g2.
  \bar "|."
}}
\header{
piece = "Grind Hans Jässpödspolska 'The Most Beautiful'"
subtitle = "after Andy Cutting"
}}
  
%{
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

