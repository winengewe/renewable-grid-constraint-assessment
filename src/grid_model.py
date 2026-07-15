import pandapower as pp


def create_constrained_33kv_network():
    """
    Creates a standard UK 132/33kV distribution network topology
    to evaluate renewable energy integration constraints.
    """
    # Initialize an empty network
    net = pp.create_empty_network(name="TNEI_Portfolio_Grid_Model")

    # 1. Create Buses (Nodes)
    # External Transmission Grid Bus (132 kV)
    b_grid = pp.create_bus(net, vn_kv=132.0, name="132kV Grid Connection")

    # Substation Primary Bus (33 kV)
    b_sub_33 = pp.create_bus(net, vn_kv=33.0, name="33kV Substation Bus")

    # Mid-line Distribution Bus (33 kV)
    b_mid_33 = pp.create_bus(net, vn_kv=33.0, name="33kV Mid-Line Bus")

    # Wind Farm Point of Common Coupling (33 kV)
    b_wpp_33 = pp.create_bus(net, vn_kv=33.0, name="33kV Wind Farm PCC")

    # 2. Create External Grid Connection (Slack Bus)
    pp.create_ext_grid(net, bus=b_grid, vm_pu=1.02, name="Transmission Slack")

    # 3. Create 132/33kV Substation Transformer (90 MVA Grid Transformer)
    pp.create_transformer_from_options(
        net,
        hv_bus=b_grid,
        lv_bus=b_sub_33,
        sn_mva=90.0,
        type="90 MVA 132/33 kV",
        name="Main Grid Transformer",
    )

    # 4. Create 33kV Distribution Lines (Using standard standard underground cables)
    # Substation to Mid-Line (10 km of 300mm2 Copper Cable)
    pp.create_line(
        net,
        from_bus=b_sub_33,
        to_bus=b_mid_33,
        length_km=10.0,
        std_type="300-A CABLE 33KV",
        name="Feeder Section 1",
    )

    # Mid-Line to Wind Farm PCC (5 km of 150mm2 Aluminum Cable)
    pp.create_line(
        net,
        from_bus=b_mid_33,
        to_bus=b_wpp_33,
        length_km=5.0,
        std_type="150-A CABLE 33KV",
        name="Feeder Section 2",
    )

    # 5. Create Local Base Demand (Static Load at Mid-Line Bus)
    pp.create_load(net, bus=b_mid_33, p_mw=15.0, q_mvar=3.0, name="Township Base Load")

    # 6. Create the 30MW Target Wind Farm (Initialized at full output)
    pp.create_sgen(net, bus=b_wpp_33, p_mw=30.0, q_mvar=0.0, name="Proposed Wind Farm")

    return net


if __name__ == "__main__":
    # Test network generation and execute a baseline snapshot load flow
    network = create_constrained_33kv_network()
    pp.runpp(network)

    print("--- Baseline Snapshot Power Flow Results ---")
    print(f"Substation Voltage: {network.res_bus.vm_pu[1]:.4f} pu")
    print(f"Wind Farm PCC Voltage: {network.res_bus.vm_pu[3]:.4f} pu")
    print(f"Feeder Section 1 Loading: {network.res_line.loading_percent[0]:.2f}%")
