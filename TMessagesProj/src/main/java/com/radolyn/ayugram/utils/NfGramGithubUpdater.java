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
import android.text.TextUtils;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import org.json.JSONArray;
import org.json.JSONObject;

public class NfGramGithubUpdater {
    public static final String GITHUB_REPO = "NothingFlare/NfGram";
    public static final String API_URL = "https://api.github.com/repos/" + GITHUB_REPO + "/releases/latest";

    private static final Handler mainHandler = new Handler(Looper.getMainLooper());
    private static boolean isChecking = false;

    public static void checkUpdates(final Object callback) {
        if (isChecking) {
            return;
        }
        isChecking = true;

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    doCheck(callback);
                } catch (Throwable t) {
                    dispatchCallback(callback, null, createTlError("NETWORK_ERROR"));
                } finally {
                    isChecking = false;
                }
            }
        }, "NfGramUpdateThread").start();
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
            if (code != 200) {
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

            String apkUrl = null;
            String apkName = null;
            if (assets != null) {
                for (int i = 0; i < assets.length(); i++) {
                    JSONObject asset = assets.getJSONObject(i);
                    String name = asset.optString("name", "");
                    if (name.toLowerCase().endsWith(".apk")) {
                        apkUrl = asset.optString("browser_download_url", null);
                        apkName = name;
                        break;
                    }
                }
            }

            String currentVersion = getCurrentVersion();
            boolean isNewer = isNewerVersion(tagName, currentVersion);

            if (isNewer && !TextUtils.isEmpty(apkUrl)) {
                final String finalApkUrl = apkUrl;
                final String finalApkName = apkName != null ? apkName : ("NfGram-" + tagName + ".apk");

                mainHandler.post(new Runnable() {
                    @Override
                    public void run() {
                        showUpdateDialog(tagName, changelog, finalApkUrl, finalApkName);
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

    private static String getCurrentVersion() {
        try {
            Class<?> bv = Class.forName("org.telegram.messenger.BuildVars");
            Field f = bv.getField("BUILD_VERSION_STRING");
            return (String) f.get(null);
        } catch (Throwable ignored) {}
        return "13.1.1";
    }

    public static boolean isNewerVersion(String releaseTag, String currentVersion) {
        if (TextUtils.isEmpty(releaseTag)) return false;
        String cleanTag = releaseTag.trim();
        if (cleanTag.startsWith("v") || cleanTag.startsWith("V")) {
            cleanTag = cleanTag.substring(1).trim();
        }
        if (TextUtils.isEmpty(currentVersion)) return false;
        String cleanCurr = currentVersion.trim();
        if (cleanCurr.startsWith("v") || cleanCurr.startsWith("V")) {
            cleanCurr = cleanCurr.substring(1).trim();
        }

        String[] tagParts = cleanTag.split("[.-]");
        String[] currParts = cleanCurr.split("[.-]");
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

    private static void showUpdateDialog(final String tagName, final String changelog, final String downloadUrl, final String apkName) {
        final Context ctx = getContext();
        if (ctx == null) return;

        if (ctx instanceof Activity && !((Activity) ctx).isFinishing()) {
            Activity act = (Activity) ctx;
            AlertDialog.Builder b = new AlertDialog.Builder(act);
            b.setTitle("Обновление NfGram (" + tagName + ")");
            String body = TextUtils.isEmpty(changelog) ? "Доступно новое обновление NfGram на GitHub!" : changelog;
            b.setMessage(body);
            b.setPositiveButton("Скачать", new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    startDownload(ctx, downloadUrl, apkName);
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
                startDownload(ctx, downloadUrl, apkName);
            }
        } else {
            startDownload(ctx, downloadUrl, apkName);
        }
    }

    public static void startDownload(final Context context, final String downloadUrl, final String fileName) {
        if (context == null || TextUtils.isEmpty(downloadUrl)) return;
        try {
            final Context appCtx = context.getApplicationContext() != null ? context.getApplicationContext() : context;
            Toast.makeText(appCtx, "NfGram: начало загрузки " + fileName, Toast.LENGTH_SHORT).show();

            DownloadManager dm = (DownloadManager) appCtx.getSystemService(Context.DOWNLOAD_SERVICE);
            if (dm != null) {
                DownloadManager.Request req = new DownloadManager.Request(Uri.parse(downloadUrl));
                req.setTitle(fileName);
                req.setDescription("Загрузка обновления NfGram с GitHub");
                req.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
                req.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, fileName);
                req.setMimeType("application/vnd.android.package-archive");

                final long downloadId = dm.enqueue(req);

                BroadcastReceiver receiver = new BroadcastReceiver() {
                    @Override
                    public void onReceive(Context c, Intent intent) {
                        long id = intent.getLongExtra(DownloadManager.EXTRA_DOWNLOAD_ID, -1);
                        if (id == downloadId) {
                            try {
                                appCtx.unregisterReceiver(this);
                            } catch (Throwable ignored) {}

                            DownloadManager m = (DownloadManager) appCtx.getSystemService(Context.DOWNLOAD_SERVICE);
                            Uri fileUri = null;
                            if (m != null) {
                                try {
                                    fileUri = m.getUriForDownloadedFile(downloadId);
                                } catch (Throwable ignored) {}
                            }
                            if (fileUri != null) {
                                Intent install = new Intent(Intent.ACTION_VIEW);
                                install.setDataAndType(fileUri, "application/vnd.android.package-archive");
                                install.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_GRANT_READ_URI_PERMISSION);
                                try {
                                    appCtx.startActivity(install);
                                } catch (Throwable e) {
                                    Toast.makeText(appCtx, "Обновление скачано в папку Загрузки: " + fileName, Toast.LENGTH_LONG).show();
                                }
                            }
                        }
                    }
                };

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
                    Method runMethod = callback.getClass().getMethod("run", Object.class, Object.class);
                    runMethod.invoke(callback, update, error);
                } catch (Throwable ignored) {}
            }
        });
    }
}
