/*
 * Copyright (C) 2026 NothingFlare
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.utils;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.DownloadManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.Uri;
import android.os.Build;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.os.ParcelFileDescriptor;
import android.provider.Settings;
import android.text.TextUtils;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.json.JSONArray;
import org.json.JSONObject;

public class NfGramGithubUpdater {
    public static final String GITHUB_REPO = "NothingFlare/NfGram";
    public static final String API_URL = "https://api.github.com/repos/" + GITHUB_REPO + "/releases/latest";

    private static final Handler mainHandler = new Handler(Looper.getMainLooper());
    private static final AtomicBoolean isChecking = new AtomicBoolean(false);
    private static BroadcastReceiver activeReceiver = null;
    private static String cachedLocalHash = null;

    public static void checkUpdates(final Object callback) {
        if (!isChecking.compareAndSet(false, true)) {
            return;
        }

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    doCheck(callback);
                } catch (Throwable t) {
                    dispatchCallback(callback, null, createTlError("NETWORK_ERROR"));
                } finally {
                    isChecking.set(false);
                }
            }
        }, "NfGramUpdateThread").start();
    }

    private static void showToast(final Context context, final String message, final boolean isLong) {
        if (context == null) return;
        mainHandler.post(new Runnable() {
            @Override
            public void run() {
                try {
                    Toast.makeText(context.getApplicationContext(), message, isLong ? Toast.LENGTH_LONG : Toast.LENGTH_SHORT).show();
                } catch (Throwable ignored) {}
            }
        });
    }

    private static void doCheck(final Object callback) {
        HttpURLConnection conn = null;
        try {
            URL url = new URL(API_URL);
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("User-Agent", "NfGram-Android");
            conn.setRequestProperty("Accept", "application/vnd.github.v3+json");
            conn.setConnectTimeout(15000);
            conn.setReadTimeout(15000);

            int code = conn.getResponseCode();
            if (code == 403) {
                showToast(getContext(), "NfGram: Лимит запросов к GitHub API исчерпан. Попробуйте позже.", true);
                dispatchCallback(callback, null, createTlError("GITHUB_RATE_LIMIT_EXCEEDED"));
                return;
            } else if (code != 200) {
                dispatchCallback(callback, null, createTlError("NO_UPDATE_METADATA"));
                return;
            }

            BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8));
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line).append('\n');
            }
            reader.close();

            JSONObject release = new JSONObject(sb.toString());
            final String tagName = release.optString("tag_name", "");
            final String changelog = release.optString("body", "");
            JSONArray assets = release.optJSONArray("assets");

            String arm64Url = null;
            String arm64Name = null;
            String universalUrl = null;
            String universalName = null;
            String telegramkeyUrl = null;
            String telegramkeyName = null;
            String apkUrl = null;
            String apkName = null;
            String shaUrl = null;

            if (assets != null) {
                for (int i = 0; i < assets.length(); i++) {
                    JSONObject asset = assets.getJSONObject(i);
                    String name = asset.optString("name", "");
                    String lower = name.toLowerCase();
                    if (lower.endsWith(".apk")) {
                        if (lower.contains("telegramkey")) {
                            telegramkeyUrl = asset.optString("browser_download_url", null);
                            telegramkeyName = name;
                        } else if (lower.contains("arm64")) {
                            arm64Url = asset.optString("browser_download_url", null);
                            arm64Name = name;
                        } else {
                            universalUrl = asset.optString("browser_download_url", null);
                            universalName = name;
                        }
                    } else if (lower.equals("sha256.txt") || lower.equals("hashes.txt") || lower.equals("checksums.txt") || lower.endsWith(".sha256")) {
                        shaUrl = asset.optString("browser_download_url", null);
                    }
                }
            }

            boolean isTelegramSigned = isTelegramKeyInstalled(getContext());
            if (isTelegramSigned && telegramkeyUrl != null) {
                apkUrl = telegramkeyUrl;
                apkName = telegramkeyName;
            } else {
                boolean is64 = Build.SUPPORTED_ABIS != null && Build.SUPPORTED_ABIS.length > 0 && Build.SUPPORTED_ABIS[0].contains("64");
                if (is64 && arm64Url != null) {
                    apkUrl = arm64Url;
                    apkName = arm64Name;
                } else if (universalUrl != null) {
                    apkUrl = universalUrl;
                    apkName = universalName;
                } else if (arm64Url != null) {
                    apkUrl = arm64Url;
                    apkName = arm64Name;
                }
            }

            // 1. Obtain remote release hash for the specific target APK
            String remoteHash = null;
            if (!TextUtils.isEmpty(shaUrl)) {
                String shaContent = fetchRemoteText(shaUrl);
                remoteHash = extractSha256ForFile(shaContent, apkName);
            }
            if (TextUtils.isEmpty(remoteHash)) {
                remoteHash = extractSha256ForFile(changelog, apkName);
            }

            // 2. Strict version comparison
            String currentVersion = getCurrentVersion();
            boolean isNewer = isNewerVersion(tagName, currentVersion);

            if (isNewer && !TextUtils.isEmpty(apkUrl)) {
                final String finalApkUrl = apkUrl;
                final String finalApkName = sanitizeApkFileName(apkName, tagName);
                final String finalRemoteHash = remoteHash;

                mainHandler.post(new Runnable() {
                    @Override
                    public void run() {
                        showUpdateDialog(tagName, changelog, finalApkUrl, finalApkName, finalRemoteHash);
                    }
                });

                dispatchCallback(callback, null, null);
            } else {
                dispatchCallback(callback, null, createTlError("NO_UPDATE_METADATA"));
            }
        } catch (Throwable t) {
            dispatchCallback(callback, null, createTlError("NETWORK_ERROR"));
        } finally {
            if (conn != null) {
                try { conn.disconnect(); } catch (Throwable ignored) {}
            }
        }
    }

    public static String getInstalledApkSha256(Context context) {
        if (cachedLocalHash != null) {
            return cachedLocalHash;
        }
        if (context == null) {
            context = getContext();
        }
        if (context == null) return null;
        try {
            String codePath = context.getPackageCodePath();
            if (TextUtils.isEmpty(codePath)) return null;
            File f = new File(codePath);
            if (!f.exists() || !f.canRead()) return null;

            MessageDigest md = MessageDigest.getInstance("SHA-256");
            FileInputStream fis = new FileInputStream(f);
            byte[] buf = new byte[65536];
            int n;
            while ((n = fis.read(buf)) != -1) {
                md.update(buf, 0, n);
            }
            fis.close();
            byte[] digest = md.digest();
            StringBuilder sb = new StringBuilder();
            for (byte b : digest) {
                sb.append(String.format("%02x", b));
            }
            cachedLocalHash = sb.toString();
            return cachedLocalHash;
        } catch (Throwable ignored) {}
        return null;
    }

    public static boolean isTelegramKeyInstalled(Context context) {
        if (context == null) context = getContext();
        if (context == null) return false;
        try {
            android.content.pm.PackageManager pm = context.getPackageManager();
            byte[] certBytes = null;
            if (Build.VERSION.SDK_INT >= 28) {
                android.content.pm.PackageInfo pi = pm.getPackageInfo(context.getPackageName(), android.content.pm.PackageManager.GET_SIGNING_CERTIFICATES);
                if (pi.signingInfo != null) {
                    android.content.pm.Signature[] sigs = pi.signingInfo.getApkContentsSigners();
                    if (sigs != null && sigs.length > 0) {
                        certBytes = sigs[0].toByteArray();
                    }
                }
            } else {
                android.content.pm.PackageInfo pi = pm.getPackageInfo(context.getPackageName(), android.content.pm.PackageManager.GET_SIGNATURES);
                if (pi.signatures != null && pi.signatures.length > 0) {
                    certBytes = pi.signatures[0].toByteArray();
                }
            }
            if (certBytes != null) {
                MessageDigest md = MessageDigest.getInstance("SHA-256");
                byte[] digest = md.digest(certBytes);
                StringBuilder sb = new StringBuilder();
                for (byte b : digest) {
                    sb.append(String.format("%02x", b));
                }
                String hash = sb.toString();
                return hash.startsWith("a08d7dc323");
            }
        } catch (Throwable ignored) {}
        return false;
    }

    public static String extractSha256(String text) {
        return extractSha256ForFile(text, null);
    }

    public static String extractSha256ForFile(String text, String fileName) {
        if (TextUtils.isEmpty(text)) return null;
        if (!TextUtils.isEmpty(fileName)) {
            try {
                Pattern pFile = Pattern.compile("([a-fA-F0-9]{64})\\s+[*]?(" + Pattern.quote(fileName) + ")|(" + Pattern.quote(fileName) + ")\\s*[:=]\\s*([a-fA-F0-9]{64})");
                Matcher mFile = pFile.matcher(text);
                if (mFile.find()) {
                    String h = mFile.group(1);
                    if (h == null) h = mFile.group(4);
                    if (h != null) return h.toLowerCase();
                }
            } catch (Throwable ignored) {}
            return null;
        }
        try {
            Pattern p = Pattern.compile("\\b([a-fA-F0-9]{64})\\b");
            Matcher m = p.matcher(text);
            if (m.find()) {
                return m.group(1).toLowerCase();
            }
        } catch (Throwable ignored) {}
        return null;
    }

    private static String fetchRemoteText(String fileUrl) {
        if (TextUtils.isEmpty(fileUrl)) return null;
        HttpURLConnection conn = null;
        try {
            URL url = new URL(fileUrl);
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setRequestProperty("User-Agent", "NfGram-Android");
            conn.setConnectTimeout(10000);
            conn.setReadTimeout(10000);
            if (conn.getResponseCode() == 200) {
                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8));
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    sb.append(line).append('\n');
                }
                reader.close();
                return sb.toString();
            }
        } catch (Throwable ignored) {
        } finally {
            if (conn != null) {
                try { conn.disconnect(); } catch (Throwable ignored) {}
            }
        }
        return null;
    }

    private static String sanitizeApkFileName(String apkName, String tagName) {
        String name = TextUtils.isEmpty(apkName) ? ("NfGram-" + tagName + ".apk") : apkName;
        name = name.replace('\\', '/');
        int lastSlash = name.lastIndexOf('/');
        if (lastSlash >= 0) {
            name = name.substring(lastSlash + 1);
        }
        name = name.replaceAll("[^a-zA-Z0-9._-]", "_");
        if (!name.toLowerCase().endsWith(".apk")) {
            name += ".apk";
        }
        return name;
    }

    private static String getCurrentVersion() {
        try {
            Class<?> bv = Class.forName("org.telegram.messenger.BuildVars");
            Field f = bv.getField("BUILD_VERSION_STRING");
            return (String) f.get(null);
        } catch (Throwable ignored) {}
        return "13.1.1";
    }

    public static boolean isNewerVersion(String releaseTag, String currentVersion) {
        if (TextUtils.isEmpty(releaseTag) || TextUtils.isEmpty(currentVersion)) return false;

        String cleanTag = releaseTag.trim();
        if (cleanTag.startsWith("v") || cleanTag.startsWith("V")) {
            cleanTag = cleanTag.substring(1).trim();
        }
        String cleanCurr = currentVersion.trim();
        if (cleanCurr.startsWith("v") || cleanCurr.startsWith("V")) {
            cleanCurr = cleanCurr.substring(1).trim();
        }

        if (cleanTag.contains(" ")) {
            cleanTag = cleanTag.split(" ")[0].trim();
        }
        if (cleanTag.contains("(")) {
            cleanTag = cleanTag.split("\\(")[0].trim();
        }
        if (cleanCurr.contains(" ")) {
            cleanCurr = cleanCurr.split(" ")[0].trim();
        }
        if (cleanCurr.contains("(")) {
            cleanCurr = cleanCurr.split("\\(")[0].trim();
        }

        String[] tagSplit = cleanTag.split("-", 2);
        String[] currSplit = cleanCurr.split("-", 2);

        String tagCore = tagSplit[0];
        String currCore = currSplit[0];

        String[] tagParts = tagCore.split("\\.");
        String[] currParts = currCore.split("\\.");
        int len = Math.max(tagParts.length, currParts.length);

        for (int i = 0; i < len; i++) {
            int tagNum = 0;
            int currNum = 0;
            if (i < tagParts.length) {
                try { tagNum = Integer.parseInt(tagParts[i].replaceAll("\\D+", "")); } catch (Exception ignored) {}
            }
            if (i < currParts.length) {
                try { currNum = Integer.parseInt(currParts[i].replaceAll("\\D+", "")); } catch (Exception ignored) {}
            }
            if (tagNum > currNum) return true;
            if (tagNum < currNum) return false;
        }

        // Pre-release tags comparison
        boolean tagHasPre = tagSplit.length > 1 && !TextUtils.isEmpty(tagSplit[1]);
        boolean currHasPre = currSplit.length > 1 && !TextUtils.isEmpty(currSplit[1]);

        if (!tagHasPre && currHasPre) {
            return true;
        }
        if (tagHasPre && !currHasPre) {
            return false;
        }
        if (tagHasPre && currHasPre) {
            int tagPreNum = 0;
            int currPreNum = 0;
            try { tagPreNum = Integer.parseInt(tagSplit[1].replaceAll("\\D+", "")); } catch (Exception ignored) {}
            try { currPreNum = Integer.parseInt(currSplit[1].replaceAll("\\D+", "")); } catch (Exception ignored) {}
            return tagPreNum > currPreNum;
        }

        return false;
    }

    private static Context getContext() {
        try {
            Class<?> la = Class.forName("org.telegram.ui.LaunchActivity");
            Field f = la.getField("instance");
            Object inst = f.get(null);
            if (inst instanceof Activity && !((Activity) inst).isFinishing()) {
                return (Activity) inst;
            }
        } catch (Throwable ignored) {}
        try {
            Class<?> al = Class.forName("org.telegram.messenger.ApplicationLoader");
            Field f = al.getField("applicationContext");
            return (Context) f.get(null);
        } catch (Throwable ignored) {}
        return null;
    }

    private static void showUpdateDialog(final String tagName, final String changelog, final String downloadUrl, final String apkName, final String remoteHash) {
        final Context ctx = getContext();
        if (ctx == null) return;

        if (ctx instanceof Activity && !((Activity) ctx).isFinishing()) {
            Activity act = (Activity) ctx;
            AlertDialog.Builder b = new AlertDialog.Builder(act);
            b.setTitle("Обновление NfGram (" + tagName + ")");

            StringBuilder bodyBuilder = new StringBuilder();
            if (!TextUtils.isEmpty(remoteHash)) {
                bodyBuilder.append("Хеш релиза (SHA-256): ").append(remoteHash.substring(0, Math.min(16, remoteHash.length()))).append("...\n\n");
            }
            if (!TextUtils.isEmpty(changelog)) {
                bodyBuilder.append(changelog);
            } else {
                bodyBuilder.append("Доступно новое обновление NfGram на GitHub!");
            }

            b.setMessage(bodyBuilder.toString());
            b.setPositiveButton("Скачать", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    startDownload(ctx, downloadUrl, apkName, remoteHash);
                    dialog.dismiss();
                }
            });
            b.setNegativeButton("Позже", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    dialog.dismiss();
                }
            });
            b.setCancelable(true);
            try {
                b.show();
            } catch (Throwable t) {
                // Ignore show failure if Activity state changed unexpectedly
            }
        } else {
            // Not in active Activity: inform user via Toast on main thread, do NOT auto-download!
            showToast(ctx, "Доступно обновление NfGram " + tagName + ". Откройте настройки для обновления.", true);
        }
    }

    public static synchronized void startDownload(final Context context, final String downloadUrl, final String fileName, final String expectedSha256) {
        if (context == null || TextUtils.isEmpty(downloadUrl)) return;
        try {
            final Context appCtx = context.getApplicationContext() != null ? context.getApplicationContext() : context;
            showToast(appCtx, "NfGram: начало загрузки " + fileName, false);

            // Delete pre-existing file in Downloads to prevent DownloadManager from appending "-1"
            try {
                File downloadsDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS);
                if (downloadsDir != null && downloadsDir.exists()) {
                    File oldFile = new File(downloadsDir, fileName);
                    if (oldFile.exists()) {
                        oldFile.delete();
                    }
                }
            } catch (Throwable ignored) {}

            // Check REQUEST_INSTALL_PACKAGES on Android 8.0+
            if (Build.VERSION.SDK_INT >= 26) {
                try {
                    if (!appCtx.getPackageManager().canRequestPackageInstalls()) {
                        Intent manageIntent = new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES);
                        manageIntent.setData(Uri.parse("package:" + appCtx.getPackageName()));
                        manageIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                        appCtx.startActivity(manageIntent);
                    }
                } catch (Throwable ignored) {}
            }

            final DownloadManager dm = (DownloadManager) appCtx.getSystemService(Context.DOWNLOAD_SERVICE);
            if (dm != null) {
                DownloadManager.Request req = new DownloadManager.Request(Uri.parse(downloadUrl));
                req.setTitle(fileName);
                req.setDescription("Загрузка обновления NfGram с GitHub");
                req.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
                req.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, fileName);
                req.setMimeType("application/vnd.android.package-archive");

                final long downloadId = dm.enqueue(req);

                if (activeReceiver != null) {
                    try {
                        appCtx.unregisterReceiver(activeReceiver);
                    } catch (Throwable ignored) {}
                    activeReceiver = null;
                }

                BroadcastReceiver receiver = new BroadcastReceiver() {
                    @Override
                    public void onReceive(Context c, Intent intent) {
                        long id = intent.getLongExtra(DownloadManager.EXTRA_DOWNLOAD_ID, -1);
                        if (id == downloadId) {
                            try {
                                appCtx.unregisterReceiver(this);
                            } catch (Throwable ignored) {}
                            synchronized (NfGramGithubUpdater.class) {
                                if (activeReceiver == this) {
                                    activeReceiver = null;
                                }
                            }

                            Uri fileUri = null;
                            try {
                                fileUri = dm.getUriForDownloadedFile(downloadId);
                            } catch (Throwable ignored) {}

                            // If expectedSha256 is present, verify downloaded file using Stream (Scoped Storage compatible)
                            if (!TextUtils.isEmpty(expectedSha256)) {
                                String actualHash = computeDownloadedHash(appCtx, dm, downloadId, fileUri, fileName);
                                if (actualHash != null && !actualHash.equalsIgnoreCase(expectedSha256)) {
                                    showToast(appCtx, "NfGram: Ошибка верификации! Хеш файла не совпадает.", true);
                                    return;
                                }
                            }

                            if (fileUri != null) {
                                Intent install = new Intent(Intent.ACTION_VIEW);
                                install.setDataAndType(fileUri, "application/vnd.android.package-archive");
                                install.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_GRANT_READ_URI_PERMISSION);
                                try {
                                    appCtx.startActivity(install);
                                } catch (Throwable e) {
                                    showToast(appCtx, "Обновление скачано в папку Загрузки: " + fileName, true);
                                }
                            } else {
                                showToast(appCtx, "Обновление сохранено в папку Загрузки: " + fileName, true);
                            }
                        }
                    }
                };

                activeReceiver = receiver;

                if (Build.VERSION.SDK_INT >= 33) {
                    appCtx.registerReceiver(receiver, new IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE), Context.RECEIVER_EXPORTED);
                } else {
                    appCtx.registerReceiver(receiver, new IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE));
                }
                return;
            }
        } catch (Throwable t) {
        }

        try {
            Intent browser = new Intent(Intent.ACTION_VIEW, Uri.parse(downloadUrl));
            browser.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            context.startActivity(browser);
        } catch (Throwable ignored) {}
    }

    private static String computeDownloadedHash(Context context, DownloadManager dm, long downloadId, Uri fileUri, String fileName) {
        InputStream is = null;
        try {
            if (fileUri != null && context != null) {
                try {
                    is = context.getContentResolver().openInputStream(fileUri);
                } catch (Throwable ignored) {}
            }
            if (is == null && dm != null) {
                try {
                    ParcelFileDescriptor pfd = dm.openDownloadedFile(downloadId);
                    if (pfd != null) {
                        is = new FileInputStream(pfd.getFileDescriptor());
                    }
                } catch (Throwable ignored) {}
            }
            if (is == null && !TextUtils.isEmpty(fileName)) {
                try {
                    File f = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS), fileName);
                    if (f.exists() && f.canRead()) {
                        is = new FileInputStream(f);
                    }
                } catch (Throwable ignored) {}
            }
            if (is != null) {
                MessageDigest md = MessageDigest.getInstance("SHA-256");
                byte[] buf = new byte[65536];
                int n;
                while ((n = is.read(buf)) != -1) {
                    md.update(buf, 0, n);
                }
                byte[] digest = md.digest();
                StringBuilder sb = new StringBuilder();
                for (byte b : digest) {
                    sb.append(String.format("%02x", b));
                }
                return sb.toString();
            }
        } catch (Throwable ignored) {
        } finally {
            if (is != null) {
                try { is.close(); } catch (Throwable ignored) {}
            }
        }
        return null;
    }

    private static Object createTlError(String text) {
        try {
            Class<?> errClass = Class.forName("org.telegram.tgnet.TLRPC$TL_error");
            Object err = errClass.getDeclaredConstructor().newInstance();
            Field tf = errClass.getField("text");
            tf.set(err, text);
            return err;
        } catch (Throwable ignored) {}
        return null;
    }

    private static void dispatchCallback(final Object callback, final Object update, final Object error) {
        if (callback == null) return;
        mainHandler.post(new Runnable() {
            @Override
            public void run() {
                try {
                    Method target = null;
                    try {
                        target = callback.getClass().getMethod("run", Object.class, Object.class);
                    } catch (Throwable t) {
                        for (Method m : callback.getClass().getMethods()) {
                            if ("run".equals(m.getName()) && m.getParameterTypes().length == 2) {
                                target = m;
                                break;
                            }
                        }
                    }
                    if (target != null) {
                        target.setAccessible(true);
                        target.invoke(callback, update, error);
                    }
                } catch (Throwable ignored) {}
            }
        });
    }
}
