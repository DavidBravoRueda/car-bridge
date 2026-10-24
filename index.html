import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class CarBridgeWebView extends StatefulWidget {
  @override
  _CarBridgeWebViewState createState() => _CarBridgeWebViewState();
}

class _CarBridgeWebViewState extends State<CarBridgeWebView> {
  late final WebViewController _controller;

  @override
  void initState() {
    super.initState();
    
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0x00000000))
      // ENGAÑAR A GOOGLE: Forzamos un User-Agent de iPhone real para evitar el captcha/bot check
      ..setUserAgent("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
      ..setNavigationDelegate(
        NavigationDelegate(
          onNavigationRequest: (NavigationRequest request) {
            final url = request.url;

            // Lista negra de dominios de anuncios de YouTube/Google para cortarlos al vuelo
            final List<String> adDomains = [
              'doubleclick.net',
              'googlesyndication.com',
              'googleads.g.doubleclick.net',
              'youtube.com/api/stats/ads',
              'pagead2.googlesyndication.com',
            ];

            for (var domain in adDomains) {
              if (url.contains(domain)) {
                return NavigationDecision.prevent; // Bloquea la publi
              }
            }

            return NavigationDecision.navigate; // Permite lo demás
          },
        ),
      )
      ..loadRequest(Uri.parse('https://www.youtube.com/tv#/')); 
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SafeArea(
        child: WebViewWidget(controller: _controller),
      ),
    );
  }
}
