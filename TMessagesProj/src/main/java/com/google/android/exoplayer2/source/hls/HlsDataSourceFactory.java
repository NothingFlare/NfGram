/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.hls;

import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.upstream.DataSource;

/** Creates {@link DataSource}s for HLS playlists, encryption and media chunks. */
public interface HlsDataSourceFactory {

  /**
   * Creates a {@link DataSource} for the given data type.
   *
   * @param dataType The {@link C.DataType} for which the {@link DataSource} will be used.
   * @return A {@link DataSource} for the given data type.
   */
  DataSource createDataSource(@C.DataType int dataType);
}
