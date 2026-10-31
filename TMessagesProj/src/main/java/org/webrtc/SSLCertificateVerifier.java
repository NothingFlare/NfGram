/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * The SSLCertificateVerifier interface allows API users to provide custom
 * logic to verify certificates.
 */
public interface SSLCertificateVerifier {
  /**
   * Implementations of verify allow applications to provide custom logic for
   * verifying certificates. This is not required by default and should be used
   * with care.
   *
   * @param certificate A byte array containing a DER encoded X509 certificate.
   * @return True if the certificate is verified and trusted else false.
   */
  @CalledByNative boolean verify(byte[] certificate);
}
