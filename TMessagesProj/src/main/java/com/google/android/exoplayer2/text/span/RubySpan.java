/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.text.span;

/**
 * A styling span for ruby text.
 *
 * <p>The text covered by this span is known as the "base text", and the ruby text is stored in
 * {@link #rubyText}.
 *
 * <p>More information on <a href="https://en.wikipedia.org/wiki/Ruby_character">ruby characters</a>
 * and <a href="https://developer.android.com/guide/topics/text/spans">span styling</a>.
 */
// NOTE: There's no Android layout support for rubies, so this span currently doesn't extend any
// styling superclasses (e.g. MetricAffectingSpan). The only way to render these rubies is to
// extract the spans and do the layout manually.
// TODO: Consider adding support for parenthetical text to be used when rendering doesn't support
// rubies (e.g. HTML <rp> tag).
public final class RubySpan implements LanguageFeatureSpan {

  /** The ruby text, i.e. the smaller explanatory characters. */
  public final String rubyText;

  /** The position of the ruby text relative to the base text. */
  public final @TextAnnotation.Position int position;

  public RubySpan(String rubyText, @TextAnnotation.Position int position) {
    this.rubyText = rubyText;
    this.position = position;
  }
}
