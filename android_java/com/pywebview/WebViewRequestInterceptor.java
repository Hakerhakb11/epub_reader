package com.pywebview;

import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;

public interface WebViewRequestInterceptor {
    WebResourceResponse shouldInterceptRequest(WebResourceRequest request);
}
