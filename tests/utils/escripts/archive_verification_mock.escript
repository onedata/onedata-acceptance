#!/usr/bin/env escript
%%! -name archive_verification_mock@test_env

-export([main/1]).

-define(NODE, list_to_atom("op_worker@dev-oneprovider-krakow-0.dev-oneprovider-krakow.default.svc.cluster.local")).

main([]) ->
    compile:file(filename:dirname(escript:script_name()) ++ "/escript_utils.erl"),
    escript_utils:connect(?NODE),
    escript_utils:safe_call(?NODE, meck, new, [archive_verification_traverse, [passthrough, no_link]]),
    escript_utils:safe_call(?NODE, meck, expect, [archive_verification_traverse, do_slave_job_unsafe,
        fun(_, _) -> throw({error, invalid_checksum}) end]).
