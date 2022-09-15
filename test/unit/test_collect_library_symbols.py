from pathlib import PosixPath
from unittest.mock import patch

import collect_library_symbols
from dso import Dso


@patch("collect_library_symbols.os")
def test_find_dsos(os_mock):
    os_mock.path.splitext().return_value(("", ".so"))
    os_mock.walk.return_value = [
        ("foo", "x", ("bar.so", "baz.so", "notadso")),
        ("foo/lal", "x", ("a.so", "b.so", "c"))
    ]

    dsos = collect_library_symbols.find_dsos("dummy")

    expected = [PosixPath('foo/bar.so'),
                PosixPath('foo/baz.so'),
                PosixPath('foo/lal/a.so'),
                PosixPath('foo/lal/b.so')]
    assert set(expected) == set(dsos)


@patch("collect_library_symbols.subprocess")
def test_get_undefined_symbols(mock_subprocess):
    mock_output = """U bar
                     w __cxa_finalize@@GLIBC_2.2.5
                     w __gmon_start__
                     w _ITM_deregisterTMCloneTable
                     w _ITM_registerTMCloneTable
                     w _Jv_RegisterClasses
                     U printf@@GLIBC_2.2.5"""
    mock_subprocess.run().stdout = mock_output

    syms = collect_library_symbols.get_undefined_symbols("dummy")

    print(f"Calls: {mock_subprocess.mock_calls}")
    assert "bar" in syms


@patch("collect_library_symbols.subprocess")
def test_get_defined_symbols(mock_subprocess):
    mock_output = """00000000000006f5 T bar
    0000000000201038 B __bss_start
    0000000000201038 b completed.6355
    0000000000000610 t deregister_tm_clones
    0000000000000680 t __do_global_dtors_aux
    0000000000200df0 t __do_global_dtors_aux_fini_array_entry
    0000000000200e00 d __dso_handle
    0000000000200e08 d _DYNAMIC
    0000000000201038 D _edata
    0000000000201040 B _end
    000000000000072c T _fini
    00000000000006c0 t frame_dummy
    0000000000200de8 t __frame_dummy_init_array_entry
    00000000000007d8 r __FRAME_END__
    0000000000201000 d _GLOBAL_OFFSET_TABLE_
    0000000000000758 r __GNU_EH_FRAME_HDR
    00000000000005a0 T _init
    0000000000200df8 d __JCR_END__
    0000000000200df8 d __JCR_LIST__
    0000000000000751 r __PRETTY_FUNCTION__.2183
    0000000000000640 t register_tm_clones
    0000000000201038 d __TMC_END__"""

    mock_subprocess.run().stdout = mock_output

    syms = collect_library_symbols.get_defined_symbols("dummy")

    assert "bar" in syms


@patch("collect_library_symbols.get_defined_symbols")
@patch("collect_library_symbols.get_undefined_symbols")
def test_get_all_symbols(mock_undef, mock_def):
    defined_syms = {"foo", "bar", "baz"}
    mock_def.return_value = defined_syms
    undefined_syms = {"a", "b", "c"}
    mock_undef.return_value = undefined_syms

    dso = collect_library_symbols.get_all_symbols("dummy")

    expected = Dso("dummy", defined_syms, undefined_syms)

    assert dso == expected
