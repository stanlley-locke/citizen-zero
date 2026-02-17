import 'package:flutter_test/flutter_test.dart';
import 'package:citizen_zero_platform/citizen_zero_platform.dart';
import 'package:citizen_zero_platform/citizen_zero_platform_platform_interface.dart';
import 'package:citizen_zero_platform/citizen_zero_platform_method_channel.dart';
import 'package:plugin_platform_interface/plugin_platform_interface.dart';

class MockCitizenZeroPlatformPlatform
    with MockPlatformInterfaceMixin
    implements CitizenZeroPlatformPlatform {

  @override
  Future<String?> getPlatformVersion() => Future.value('42');
}

void main() {
  final CitizenZeroPlatformPlatform initialPlatform = CitizenZeroPlatformPlatform.instance;

  test('$MethodChannelCitizenZeroPlatform is the default instance', () {
    expect(initialPlatform, isInstanceOf<MethodChannelCitizenZeroPlatform>());
  });

  test('getPlatformVersion', () async {
    CitizenZeroPlatform citizenZeroPlatformPlugin = CitizenZeroPlatform();
    MockCitizenZeroPlatformPlatform fakePlatform = MockCitizenZeroPlatformPlatform();
    CitizenZeroPlatformPlatform.instance = fakePlatform;

    expect(await citizenZeroPlatformPlugin.getPlatformVersion(), '42');
  });
}
