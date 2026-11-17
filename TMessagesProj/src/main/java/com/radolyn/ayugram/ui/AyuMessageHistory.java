/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.ui;

import android.content.Context;
import android.text.TextUtils;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.radolyn.ayugram.AyuConstants;
import com.radolyn.ayugram.database.entities.EditedMessage;
import com.radolyn.ayugram.messages.AyuMessagesController;
import com.radolyn.ayugram.proprietary.AyuMessageUtils;
import org.telegram.messenger.*;
import org.telegram.tgnet.TLRPC;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.ActionBar.Theme;
import org.telegram.ui.ActionBar.ThemeDescription;
import org.telegram.ui.Components.LayoutHelper;
import org.telegram.ui.Components.RecyclerListView;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class AyuMessageHistory extends BaseFragment implements NotificationCenter.NotificationCenterDelegate {
    private final MessageObject messageObject;
    private List<EditedMessage> messages;
    private int rowCount;
    private RecyclerListView listView;

    public AyuMessageHistory(MessageObject messageObject) {
        this.messageObject = messageObject;

        updateHistory();
    }

    private void updateHistory() {
        if (messageObject == null) {
            messages = new ArrayList<>();
            rowCount = 0;
            return;
        }
        var messagesController = AyuMessagesController.getInstance();
        long dialogId = messageObject.getDialogId();
        int messageId = messageObject.getId();
        messages = messagesController.getRevisions(getUserConfig().clientUserId, dialogId, messageId);
        if (messages == null) {
            messages = new ArrayList<>();
        }
        rowCount = messages.size();
    }

    @Override
    public View createView(Context context) {
        String name = null;
        String subtitle = "";
        if (messages != null && !messages.isEmpty()) {
            var firstMsg = messages.get(0);
            var peer = getMessagesController().getUserOrChat(firstMsg.dialogId);
            subtitle = String.valueOf(firstMsg.messageId);

            if (peer == null) {
                name = "?";
            } else if (peer instanceof TLRPC.User) {
                name = UserObject.getUserName((TLRPC.User) peer);
            } else if (peer instanceof TLRPC.Chat) {
                name = ((TLRPC.Chat) peer).title;
            } else {
                name = LocaleController.getString("EditsHistoryTitle", R.string.EditsHistoryTitle);
            }
        }
        if (TextUtils.isEmpty(name)) {
            name = LocaleController.getString("EditsHistoryTitle", R.string.EditsHistoryTitle);
        }

        actionBar.setBackButtonImage(R.drawable.ic_ab_back);
        actionBar.setAllowOverlayTitle(true);
        actionBar.setTitle(name);
        if (!subtitle.isEmpty()) {
            actionBar.setSubtitle(subtitle);
        }
        actionBar.setActionBarMenuOnItemClick(new ActionBar.ActionBarMenuOnItemClick() {
            @Override
            public void onItemClick(int id) {
                if (id == -1) {
                    finishFragment();
                }
            }
        });

        fragmentView = new FrameLayout(context);
        FrameLayout frameLayout = (FrameLayout) fragmentView;
        frameLayout.setBackgroundColor(Theme.getColor(Theme.key_windowBackgroundGray));

        listView = new RecyclerListView(context);
        listView.setItemAnimator(null);
        listView.setLayoutManager(new LinearLayoutManager(context, LinearLayoutManager.VERTICAL, false));
        frameLayout.addView(listView, LayoutHelper.createFrame(LayoutHelper.MATCH_PARENT, LayoutHelper.MATCH_PARENT));
        ListAdapter adapter;
        listView.setAdapter(adapter = new AyuMessageHistory.ListAdapter(context));

        return fragmentView;
    }

    @Override
    public ArrayList<ThemeDescription> getThemeDescriptions() {
        return new ArrayList<>();
    }

    @Override
    public boolean onFragmentCreate() {
        super.onFragmentCreate();

        NotificationCenter.getInstance(currentAccount).addObserver(this, AyuConstants.MESSAGE_EDITED_NOTIFICATION);

        return true;
    }

    @Override
    public void didReceivedNotification(int id, int account, Object... args) {
        if (id == AyuConstants.MESSAGE_EDITED_NOTIFICATION) {
            if (args != null && args.length >= 2 && messageObject != null) {
                var dialogId = (long) args[0];
                var messageId = (int) args[1];

                if (dialogId == messageObject.getDialogId() && messageId == messageObject.getId()) {
                    AndroidUtilities.runOnUIThread(() -> {
                        updateHistory();
                        if (listView != null && listView.getAdapter() != null) {
                            listView.getAdapter().notifyDataSetChanged();
                        }
                    });
                }
            }
        }
    }

    @Override
    public void onFragmentDestroy() {
        super.onFragmentDestroy();

        NotificationCenter.getInstance(currentAccount).removeObserver(this, AyuConstants.MESSAGE_EDITED_NOTIFICATION);
    }

    private class ListAdapter extends RecyclerListView.SelectionAdapter {

        private final Context context;

        public ListAdapter(Context context) {
            this.context = context;
        }

        @Override
        public boolean isEnabled(RecyclerView.ViewHolder holder) {
            return true;
        }

        @Override
        public int getItemCount() {
            return rowCount;
        }

        @Override
        public RecyclerView.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
            View view;
            if (viewType == 1) {
                view = new AyuMessageCell(context, getParentActivity(), AyuMessageHistory.this);
            } else {
                view = new View(context);
                view.setLayoutParams(new RecyclerView.LayoutParams(0, 0));
            }
            return new RecyclerListView.Holder(view);
        }

        @Override
        public void onBindViewHolder(RecyclerView.ViewHolder holder, int position) {
            if (holder.getItemViewType() == 1 && position >= 0 && messages != null && position < messages.size()) {
                var ayuMessageDetailCell = (AyuMessageCell) holder.itemView;

                var editedMessage = messages.get(position);
                var msg = createMessageObject(editedMessage);

                ayuMessageDetailCell.setMessageObject(msg, null, false, false);
                ayuMessageDetailCell.setEditedMessage(editedMessage);
                ayuMessageDetailCell.setId(position);
            }
        }

        @Override
        public int getItemViewType(int position) {
            return position >= 0 && messages != null && position < messages.size() ? 1 : 0;
        }

        private MessageObject createMessageObject(EditedMessage editedMessage) {
            // shamefully copied from Extera's sticker size preview
            var msg = new TLRPC.TL_message();
            AyuMessageUtils.map(editedMessage, msg, currentAccount);
            AyuMessageUtils.mapMedia(editedMessage, msg);

            msg.date = editedMessage.entityCreateDate;
            msg.edit_hide = true;

            // fix media state if available
            if (msg.media == null && messageObject != null && messageObject.messageOwner != null && messageObject.messageOwner.media != null) {
                msg.media = messageObject.messageOwner.media;
            }

            // let file be downloaded
            if (editedMessage.documentType == AyuConstants.DOCUMENT_TYPE_FILE && messageObject != null && messageObject.messageOwner != null) {
                java.io.File pathFile = FileLoader.getInstance(currentAccount).getPathToMessage(messageObject.messageOwner);
                if (pathFile != null && Objects.equals(editedMessage.mediaPath, pathFile.getAbsolutePath())) {
                    if (messageObject.messageOwner.media != null && msg.media != null) {
                        msg.media.document = messageObject.messageOwner.media.document;
                    }
                }
            }

            // fix reply state
            if (messageObject != null && messageObject.messageOwner != null && messageObject.messageOwner.replyMessage != null) {
                msg.replyMessage = messageObject.messageOwner.replyMessage;
                msg.reply_to = messageObject.messageOwner.reply_to;
            }

            return new MessageObject(getCurrentAccount(), msg, false, true);
        }
    }
}
