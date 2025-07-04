patterns = {
    'x86_64': [
        {
            "id": 1,
            "start": b'\x49\x3B\x66\x10\x0F\x86',
            "end": rb'\xE8...\xFF\x48\x83\xC4.\x5D\xC3',
            "details": 'Own research, Mach-O x64 samples - DDosia'
        },
        {
            "id": 2,
            "start": b'\x49\x3B\x66\x10\x0F\x86',
            "end": rb'\xE8...\xFF\x48\x8B\x6C\x24.\x48\x83\xC4.\xC3',
            "details": 'Own research, Mach-O x64 samples - Sliver'
        }
    ],

    'arm64': [
        {
            "id": 2,
            "start": b'\x90\x0B\x40\xF9\xFF\x63',
            "end": rb'\x97\xFD\xFB\x7F\xA9\xFF..\x91\xC0\x03\x5F\xD6',
            "details": 'Own research, Mach-O ARM64 samples'
        }
    ]
}
