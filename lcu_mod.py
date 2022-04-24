import pymeow

effect_queue = []

effect_text = {
    1001: "Kill Player(s)"
}

effect_reference = {
    "(insert redemption id here)": 1001
}

async def read_offsets(proc, base_address, offsets):
    basepoint = pymeow.read_int64(proc, base_address)

    current_pointer = basepoint

    for i in offsets[:-1]:
        current_pointer = pymeow.read_int64(proc, current_pointer+i)
    
    return current_pointer + offsets[-1]

async def reload_addrs():
    global data_addr
    try:
        data_base_addr   = proc["modules"]["LEGOLCUR_DX11.exe"]["baseaddr"] + 0x017ECA08
        data_addr = await read_offsets(proc, data_base_addr, [0x48, 0x60, 0x68, 0x38, 0x88])
    except:
        print("[WARNING] Failed to load addresses - if you're on the title screen or loading into a level, you can ignore this message.")
        return False

async def get_data_value():
    return pymeow.read_int(proc, data_addr)

async def write_data_value(value: int, wait: bool = False):
    pymeow.write_int(proc, data_addr, value)
    if wait: await wait_until_ready()

async def wait_until_ready():
    while await get_data_value() != 1000: pass

async def initialise():
    global proc
    try:
        proc = pymeow.process_by_name("LEGOLCUR_DX11.exe")
    except:
        raise Exception("Error: failed to find process! Make sure LCU is running!")

    await reload_addrs()

if __name__ == "__main__":
    print("This is the wrong file! Please run `bot.py` instead!")
    input()
    exit()