/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.drm;

import static com.google.android.exoplayer2.drm.DefaultDrmSessionManager.MODE_PLAYBACK;
import static com.google.android.exoplayer2.util.Assertions.checkNotNull;

import androidx.annotation.GuardedBy;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import com.google.android.exoplayer2.MediaItem;
import com.google.android.exoplayer2.upstream.DataSource;
import com.google.android.exoplayer2.upstream.DefaultHttpDataSource;
import com.google.android.exoplayer2.util.Util;
import com.google.common.primitives.Ints;
import java.util.Map;
import org.checkerframework.checker.nullness.qual.MonotonicNonNull;

/** Default implementation of {@link DrmSessionManagerProvider}. */
public final class DefaultDrmSessionManagerProvider implements DrmSessionManagerProvider {

  private final Object lock;

  @GuardedBy("lock")
  private MediaItem.@MonotonicNonNull DrmConfiguration drmConfiguration;

  @GuardedBy("lock")
  private @MonotonicNonNull DrmSessionManager manager;

  @Nullable private DataSource.Factory drmHttpDataSourceFactory;
  @Nullable private String userAgent;

  public DefaultDrmSessionManagerProvider() {
    lock = new Object();
  }

  /**
   * Sets the {@link DataSource.Factory} which is used to create {@link HttpMediaDrmCallback}
   * instances. If {@code null} is passed a {@link DefaultHttpDataSource.Factory} is used.
   *
   * @param drmDataSourceFactory The data source factory or {@code null} to use {@link
   *     DefaultHttpDataSource.Factory}.
   */
  public void setDrmHttpDataSourceFactory(@Nullable DataSource.Factory drmDataSourceFactory) {
    this.drmHttpDataSourceFactory = drmDataSourceFactory;
  }

  /**
   * @deprecated Pass a custom {@link DataSource.Factory} to {@link
   *     #setDrmHttpDataSourceFactory(DataSource.Factory)} which sets the desired user agent on
   *     outgoing requests.
   */
  @Deprecated
  public void setDrmUserAgent(@Nullable String userAgent) {
    this.userAgent = userAgent;
  }

  @Override
  public DrmSessionManager get(MediaItem mediaItem) {
    checkNotNull(mediaItem.localConfiguration);
    @Nullable
    MediaItem.DrmConfiguration drmConfiguration = mediaItem.localConfiguration.drmConfiguration;
    if (drmConfiguration == null || Util.SDK_INT < 18) {
      return DrmSessionManager.DRM_UNSUPPORTED;
    }

    synchronized (lock) {
      if (!Util.areEqual(drmConfiguration, this.drmConfiguration)) {
        this.drmConfiguration = drmConfiguration;
        this.manager = createManager(drmConfiguration);
      }
      return checkNotNull(this.manager);
    }
  }

  @RequiresApi(18)
  private DrmSessionManager createManager(MediaItem.DrmConfiguration drmConfiguration) {
    DataSource.Factory dataSourceFactory =
        drmHttpDataSourceFactory != null
            ? drmHttpDataSourceFactory
            : new DefaultHttpDataSource.Factory().setUserAgent(userAgent);
    HttpMediaDrmCallback httpDrmCallback =
        new HttpMediaDrmCallback(
            drmConfiguration.licenseUri == null ? null : drmConfiguration.licenseUri.toString(),
            drmConfiguration.forceDefaultLicenseUri,
            dataSourceFactory);
    for (Map.Entry<String, String> entry : drmConfiguration.licenseRequestHeaders.entrySet()) {
      httpDrmCallback.setKeyRequestProperty(entry.getKey(), entry.getValue());
    }
    DefaultDrmSessionManager drmSessionManager =
        new DefaultDrmSessionManager.Builder()
            .setUuidAndExoMediaDrmProvider(
                drmConfiguration.scheme, FrameworkMediaDrm.DEFAULT_PROVIDER)
            .setMultiSession(drmConfiguration.multiSession)
            .setPlayClearSamplesWithoutKeys(drmConfiguration.playClearContentWithoutKey)
            .setUseDrmSessionsForClearContent(
                Ints.toArray(drmConfiguration.forcedSessionTrackTypes))
            .build(httpDrmCallback);
    drmSessionManager.setMode(MODE_PLAYBACK, drmConfiguration.getKeySetId());
    return drmSessionManager;
  }
}
