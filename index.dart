import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Car Bridge',
      theme: ThemeData.dark(),
      home: const CarBridgeScreen(),
    );
  }
}

class CarBridgeScreen extends StatefulWidget {
  const CarBridgeScreen({super.key});

  @override
  State<CarBridgeScreen> createState() => _CarBridgeScreenState();
}

class _CarBridgeScreenState extends State<CarBridgeScreen> {
  late final WebViewController _controller;

  @override
  void initState() {
    super.initState();
    
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0x00000000))
      // Forzamos el User-Agent de iPhone real para saltarnos el bloqueo de YouTube
      ..setUserAgent("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
      ..setNavigationDelegate(
        NavigationDelegate(
          onNavigationRequest: (NavigationRequest request) {
            final url = request.url;

            // Cortamos al vuelo los dominios de anuncios de Google/YouTube
            final List<String> adDomains = [
              'doubleclick.net',
              'googlesyndication.com',
              'googleads.g.doubleclick.net',
              'youtube.com/api/stats/ads',
              'pagead2.googlesyndication.com',
            ];

            for (var domain in adDomains) {
              if (url.contains(domain)) {
                return NavigationDecision.prevent; // Bloquea el anuncio
              }
            }

            return NavigationDecision.navigate; // Deja pasar el vídeo limpio
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
