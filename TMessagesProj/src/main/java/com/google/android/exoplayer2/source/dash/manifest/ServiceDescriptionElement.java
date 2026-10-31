/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.dash.manifest;

import com.google.android.exoplayer2.C;

/** Represents a service description element. */
public final class ServiceDescriptionElement {

  /** The target live offset in milliseconds, or {@link C#TIME_UNSET} if undefined. */
  public final long targetOffsetMs;
  /** The minimum live offset in milliseconds, or {@link C#TIME_UNSET} if undefined. */
  public final long minOffsetMs;
  /** The maximum live offset in milliseconds, or {@link C#TIME_UNSET} if undefined. */
  public final long maxOffsetMs;
  /**
   * The minimum factor by which playback can be sped up for live speed adjustment, or {@link
   * C#RATE_UNSET} if undefined.
   */
  public final float minPlaybackSpeed;
  /**
   * The maximum factor by which playback can be sped up for live speed adjustment, or {@link
   * C#RATE_UNSET} if undefined.
   */
  public final float maxPlaybackSpeed;

  /**
   * Creates a service description element.
   *
   * @param targetOffsetMs The target live offset in milliseconds, or {@link C#TIME_UNSET} if
   *     undefined.
   * @param minOffsetMs The minimum live offset in milliseconds, or {@link C#TIME_UNSET} if
   *     undefined.
   * @param maxOffsetMs The maximum live offset in milliseconds, or {@link C#TIME_UNSET} if
   *     undefined.
   * @param minPlaybackSpeed The minimum factor by which playback can be sped up for live speed
   *     adjustment, or {@link C#RATE_UNSET} if undefined.
   * @param maxPlaybackSpeed The maximum factor by which playback can be sped up for live speed
   *     adjustment, or {@link C#RATE_UNSET} if undefined.
   */
  public ServiceDescriptionElement(
      long targetOffsetMs,
      long minOffsetMs,
      long maxOffsetMs,
      float minPlaybackSpeed,
      float maxPlaybackSpeed) {
    this.targetOffsetMs = targetOffsetMs;
    this.minOffsetMs = minOffsetMs;
    this.maxOffsetMs = maxOffsetMs;
    this.minPlaybackSpeed = minPlaybackSpeed;
    this.maxPlaybackSpeed = maxPlaybackSpeed;
  }
}
