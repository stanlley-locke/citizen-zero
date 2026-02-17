import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:citizen_zero_platform/citizen_zero_platform_method_channel.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  MethodChannelCitizenZeroPlatform platform = MethodChannelCitizenZeroPlatform();
  const MethodChannel channel = MethodChannel('citizen_zero_platform');

  setUp(() {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(
      channel,
      (MethodCall methodCall) async {
        return '42';
      },
    );
  });

  tearDown(() {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger.setMockMethodCallHandler(channel, null);
  });

  test('getPlatformVersion', () async {
    expect(await platform.getPlatformVersion(), '42');
  });
}
