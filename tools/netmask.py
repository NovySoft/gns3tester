def netmask_to_cidr(netmask):
    """Convert a netmask in dotted-decimal notation to CIDR notation."""
    if netmask == 'Unassigned' or netmask == 'Unknown' or netmask.count('.') != 3:
        return 'Err'
    return sum(bin(int(x)).count('1') for x in netmask.split('.'))