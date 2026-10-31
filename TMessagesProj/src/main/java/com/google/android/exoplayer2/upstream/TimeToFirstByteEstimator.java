/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.upstream;

import com.google.android.exoplayer2.C;

/** Provides an estimate of the time to first byte of a transfer. */
public interface TimeToFirstByteEstimator {
  /**
   * Returns the estimated time to first byte of the response body, in microseconds, or {@link
   * C#TIME_UNSET} if no estimate is available.
   */
  long getTimeToFirstByteEstimateUs();

  /** Resets the estimator. */
  void reset();

  /**
   * Called when a transfer is being initialized.
   *
   * @param dataSpec Describes the data for which the transfer is initialized.
   */
  void onTransferInitializing(DataSpec dataSpec);

  /**
   * Called when a transfer starts.
   *
   * @param dataSpec Describes the data being transferred.
   */
  void onTransferStart(DataSpec dataSpec);
}
