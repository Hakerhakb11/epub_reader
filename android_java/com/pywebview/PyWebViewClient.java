package com.pywebview;

import android.graphics.Bitmap;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;

public class PyWebViewClient extends WebViewClient {
    private EventCallbackWrapper callbackWrapper;
    private WebViewRequestInterceptor requestInterceptor;
    private boolean jsInject;

    public void setCallback(EventCallbackWrapper callbackWrapper, boolean jsInject) {
        this.callbackWrapper = callbackWrapper;
        this.jsInject = jsInject;
    }

    public void setRequestInterceptor(WebViewRequestInterceptor requestInterceptor) {
        this.requestInterceptor = requestInterceptor;
    }

    @Override
    public void onPageStarted(WebView view, String url, Bitmap favicon) {
        super.onPageStarted(view, url, favicon);
        if (callbackWrapper != null) {
            callbackWrapper.onPageStarted(url);
        }
    }

    @Override
    public void onPageFinished(WebView view, String url) {
        super.onPageFinished(view, url);
        if (callbackWrapper != null) {
            callbackWrapper.onPageFinished(url);
        }
    }

    @Override
    public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
        if (requestInterceptor != null) {
            WebResourceResponse response = requestInterceptor.shouldInterceptRequest(request);
            if (response != null) {
                return response;
            }
        }
        return super.shouldInterceptRequest(view, request);
    }
}
