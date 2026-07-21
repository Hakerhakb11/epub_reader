package com.pywebview;

public interface EventCallbackWrapper {
    void onPageStarted(String url);
    void onPageFinished(String url);
}
