#!/usr/bin/env escript
%%! -name oc_test@test_env

-export([main/1]).

safe_call(Node, Module, Function, Args) ->
    true = net_kernel:hidden_connect_node(Node),
    case rpc:call(Node, Module, Function, Args) of
        {badrpc, X} ->
            io:format(standard_error, "ERROR: in module ~p:~n {badrpc, ~p} in rpc:call(~p, ~p, ~p, ~p).~n",
                [?MODULE, X, Node, Module, Function, Args]),
            halt(42);
        {error, X} ->
            io:format(standard_error, "ERROR: in module ~p:~n {error, ~p} in rpc:call(~p, ~p, ~p, ~p).~n",
                [?MODULE, X, Node, Module, Function, Args]),
            halt(42);
        X ->
            X
    end.

main([Duration]) ->
        Node = "op_worker@dev-oneprovider-krakow-0.dev-oneprovider-krakow.default.svc.cluster.local",
        NodeAtom = list_to_atom(Node),
        erlang:set_cookie(NodeAtom, cluster_node),
        safe_call(NodeAtom, https_listener, stop, []),
        DurationInt = list_to_integer(Duration),
        timer:sleep(timer:seconds(DurationInt)),
        safe_call(NodeAtom, https_listener, start, []).
