"""Run with Python + PyYAML: python -m unittest discover -s tests -v."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/generate_clash_profile.mjs'
FIXTURE = ROOT / 'tests/fixture.env.example'


class GeneratorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name) / 'profile.yaml'

    def generate(self, *args):
        result = subprocess.run(['node', str(SCRIPT), *map(str, args), '--out', str(self.out)],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(os.stat(self.out).st_mode & 0o777, 0o600)
        return yaml.safe_load(self.out.read_text())

    def test_template_is_credential_free_and_accepts_dynamic_nodes(self):
        config = self.generate('--subscription-template')
        self.assertNotIn('proxies', config)
        encoded = json.dumps(config)
        for forbidden in ('uuid', 'public-key', 'short-id', 'subscription-test-', '203.0.113.10'):
            self.assertNotIn(forbidden, encoded)
        groups = {g['name']: g for g in config['proxy-groups']}
        self.assertTrue(groups['PROXY']['include-all'])
        self.assertEqual(groups['节点选择']['proxies'][0], 'PROXY')
        for group in groups.values():
            for name in group.get('proxies', []):
                self.assertIn(name, set(groups) | {'DIRECT'})
        self.assertIn('GEOSITE,cn,DIRECT', config['rules'])
        self.assertEqual(config['rules'][-1], 'MATCH,其他海外')
        self.assertFalse(config['tun']['enable'])
        self.assertEqual(config['dns']['listen'], '127.0.0.1:1053')

    def test_template_rejects_credentials_and_test_mode_without_writing(self):
        for args in [('--env', str(FIXTURE)), ('--uri-file', str(FIXTURE)), ('--test',)]:
            with self.subTest(args=args):
                result = subprocess.run(['node', str(SCRIPT), '--subscription-template',
                                         *args, '--out', str(self.out)], capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.out.exists())

    def test_existing_profile_keeps_fixture_node_and_routing(self):
        config = self.generate('--env', FIXTURE)
        node = config['proxies'][0]
        self.assertEqual(node['server'], '203.0.113.10')
        self.assertEqual(node['uuid'], '11111111-1111-4111-8111-111111111111')
        self.assertEqual(config['proxy-groups'][0]['proxies'][0], node['name'])
        self.assertEqual(config['rules'][-1], 'MATCH,其他海外')

    def test_existing_test_mode_is_isolated(self):
        config = self.generate('--env', FIXTURE, '--test', '--mixed-port', '17930')
        self.assertEqual(config['mixed-port'], 17930)
        self.assertFalse(config['tun']['enable'])
        self.assertFalse(config['geo-auto-update'])
        self.assertEqual(config['dns']['listen'], '127.0.0.1:11053')

    def test_existing_private_output_permissions_are_tightened(self):
        self.out.write_text('previous')
        self.out.chmod(0o644)
        self.generate('--subscription-template')


if __name__ == '__main__':
    unittest.main()
