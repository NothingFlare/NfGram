/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.smoothstreaming;

import androidx.annotation.Nullable;
import com.google.android.exoplayer2.source.chunk.ChunkSource;
import com.google.android.exoplayer2.source.smoothstreaming.manifest.SsManifest;
import com.google.android.exoplayer2.trackselection.ExoTrackSelection;
import com.google.android.exoplayer2.upstream.LoaderErrorThrower;
import com.google.android.exoplayer2.upstream.TransferListener;

/** A {@link ChunkSource} for SmoothStreaming. */
public interface SsChunkSource extends ChunkSource {

  /** Factory for {@link SsChunkSource}s. */
  interface Factory {

    /**
     * Creates a new {@link SsChunkSource}.
     *
     * @param manifestLoaderErrorThrower Throws errors affecting loading of manifests.
     * @param manifest The initial manifest.
     * @param streamElementIndex The index of the corresponding stream element in the manifest.
     * @param trackSelection The track selection.
     * @param transferListener The transfer listener which should be informed of any data transfers.
     *     May be null if no listener is available.
     * @return The created {@link SsChunkSource}.
     */
    SsChunkSource createChunkSource(
        LoaderErrorThrower manifestLoaderErrorThrower,
        SsManifest manifest,
        int streamElementIndex,
        ExoTrackSelection trackSelection,
        @Nullable TransferListener transferListener);
  }

  /**
   * Updates the manifest.
   *
   * @param newManifest The new manifest.
   */
  void updateManifest(SsManifest newManifest);

  /**
   * Updates the track selection.
   *
   * @param trackSelection The new track selection instance. Must be equivalent to the previous one.
   */
  void updateTrackSelection(ExoTrackSelection trackSelection);
}
