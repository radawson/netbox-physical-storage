"""
RAID calculation utilities for capacity and failure tolerance calculations.
Supports all standard RAID levels as defined in:
https://en.wikipedia.org/wiki/Standard_RAID_levels
"""

from decimal import Decimal
from typing import Optional, List


def calculate_raid_capacity(raid_level: str, drive_sizes: List[Decimal], drive_count: int) -> Optional[dict]:
    """
    Calculate usable capacity for a RAID configuration.
    
    Args:
        raid_level: RAID level (e.g., 'RAID0', 'RAID5', 'RAID6')
        drive_sizes: List of drive sizes in GB
        drive_count: Total number of drives
    
    Returns:
        Dictionary with 'capacity_gb' (Decimal) and 'formatted' (string) keys, or None if invalid
    """
    if not drive_sizes or drive_count == 0:
        return None
    
    # Use smallest drive size for capacity calculations (RAID standard)
    min_size = min(drive_sizes)
    
    if raid_level == 'RAID0':
        # RAID 0: Striping, no redundancy, capacity = sum of all drives
        capacity = sum(drive_sizes)
    
    elif raid_level == 'RAID1':
        # RAID 1: Mirroring, capacity = smallest drive
        capacity = min_size
    
    elif raid_level in ('RAID2', 'RAID3', 'RAID4'):
        # RAID 2/3/4: Parity-based, capacity = (n-1) * smallest drive
        if drive_count < 2:
            return None
        capacity = (drive_count - 1) * min_size
    
    elif raid_level == 'RAID5':
        # RAID 5: Single parity, capacity = (n-1) * smallest drive
        if drive_count < 3:
            return None
        capacity = (drive_count - 1) * min_size
    
    elif raid_level == 'RAID6':
        # RAID 6: Dual parity, capacity = (n-2) * smallest drive
        if drive_count < 4:
            return None
        capacity = (drive_count - 2) * min_size
    
    elif raid_level == 'RAID10':
        # RAID 10: Mirrored stripes, capacity = (n/2) * smallest drive
        if drive_count < 2 or drive_count % 2 != 0:
            return None
        capacity = (drive_count / 2) * min_size
    
    elif raid_level == 'RAID01':
        # RAID 01: Striped mirrors, capacity = (n/2) * smallest drive
        if drive_count < 2 or drive_count % 2 != 0:
            return None
        capacity = (drive_count / 2) * min_size
    
    elif raid_level == 'RAID50':
        # RAID 50: RAID 5 with striping
        # For simplicity, assume 2 RAID 5 arrays striped
        # Each array needs at least 3 drives, so minimum 6 drives total
        if drive_count < 6 or drive_count % 2 != 0:
            return None
        # Each RAID 5 array has drive_count/2 drives
        # Capacity per array: ((drive_count/2) - 1) * min_size
        # Total capacity: 2 * capacity_per_array
        drives_per_array = drive_count // 2
        capacity_per_array = (drives_per_array - 1) * min_size
        capacity = 2 * capacity_per_array
    
    elif raid_level == 'RAID60':
        # RAID 60: RAID 6 with striping
        # For simplicity, assume 2 RAID 6 arrays striped
        # Each array needs at least 4 drives, so minimum 8 drives total
        if drive_count < 8 or drive_count % 2 != 0:
            return None
        # Each RAID 6 array has drive_count/2 drives
        # Capacity per array: ((drive_count/2) - 2) * min_size
        # Total capacity: 2 * capacity_per_array
        drives_per_array = drive_count // 2
        capacity_per_array = (drives_per_array - 2) * min_size
        capacity = 2 * capacity_per_array
    
    else:
        return None
    
    # Format capacity for display
    formatted = format_capacity(capacity)
    
    return {
        'capacity_gb': capacity,
        'formatted': formatted
    }


def calculate_raid_failure_tolerance(raid_level: str, drive_count: int) -> Optional[dict]:
    """
    Calculate failure tolerance for a RAID configuration.
    
    Args:
        raid_level: RAID level (e.g., 'RAID0', 'RAID5', 'RAID6')
        drive_count: Total number of drives
    
    Returns:
        Dictionary with 'tolerance' (int) and 'description' (string) keys, or None if invalid
    """
    if drive_count == 0:
        return None
    
    if raid_level == 'RAID0':
        # RAID 0: No redundancy, any failure causes data loss
        return {
            'tolerance': 0,
            'description': 'No redundancy - any drive failure causes data loss'
        }
    
    elif raid_level == 'RAID1':
        # RAID 1: Mirroring, can lose all but one drive
        tolerance = drive_count - 1
        return {
            'tolerance': tolerance,
            'description': f'Can tolerate {tolerance} drive failure(s)'
        }
    
    elif raid_level in ('RAID2', 'RAID3', 'RAID4'):
        # RAID 2/3/4: Single parity, can lose 1 drive
        if drive_count < 2:
            return None
        return {
            'tolerance': 1,
            'description': 'Can tolerate 1 drive failure'
        }
    
    elif raid_level == 'RAID5':
        # RAID 5: Single parity, can lose 1 drive
        if drive_count < 3:
            return None
        return {
            'tolerance': 1,
            'description': 'Can tolerate 1 drive failure'
        }
    
    elif raid_level == 'RAID6':
        # RAID 6: Dual parity, can lose 2 drives
        if drive_count < 4:
            return None
        return {
            'tolerance': 2,
            'description': 'Can tolerate 2 drive failures'
        }
    
    elif raid_level == 'RAID10':
        # RAID 10: Mirrored stripes, can lose 1 drive per mirror pair
        if drive_count < 2 or drive_count % 2 != 0:
            return None
        # Can lose one drive from each mirror pair
        tolerance = drive_count // 2
        return {
            'tolerance': tolerance,
            'description': f'Can tolerate {tolerance} drive failure(s) (1 per mirror pair)'
        }
    
    elif raid_level == 'RAID01':
        # RAID 01: Striped mirrors, can lose 1 drive per mirror pair
        if drive_count < 2 or drive_count % 2 != 0:
            return None
        tolerance = drive_count // 2
        return {
            'tolerance': tolerance,
            'description': f'Can tolerate {tolerance} drive failure(s) (1 per mirror pair)'
        }
    
    elif raid_level == 'RAID50':
        # RAID 50: RAID 5 with striping, can lose 1 drive per RAID 5 array
        if drive_count < 6 or drive_count % 2 != 0:
            return None
        # 2 RAID 5 arrays, can lose 1 from each
        tolerance = 2
        return {
            'tolerance': tolerance,
            'description': 'Can tolerate 2 drive failures (1 per RAID 5 array)'
        }
    
    elif raid_level == 'RAID60':
        # RAID 60: RAID 6 with striping, can lose 2 drives per RAID 6 array
        if drive_count < 8 or drive_count % 2 != 0:
            return None
        # 2 RAID 6 arrays, can lose 2 from each
        tolerance = 4
        return {
            'tolerance': tolerance,
            'description': 'Can tolerate 4 drive failures (2 per RAID 6 array)'
        }
    
    return None


def format_capacity(capacity_gb: Decimal) -> str:
    """
    Format capacity in GB to a human-readable string.
    
    Args:
        capacity_gb: Capacity in GB (Decimal)
    
    Returns:
        Formatted string (e.g., "80 TB" or "1.5 GB")
    """
    capacity = float(capacity_gb)
    
    if capacity >= 1024 * 1024:  # >= 1 PB
        return f"{capacity / (1024 * 1024):.2f} PB"
    elif capacity >= 1024:  # >= 1 TB
        return f"{capacity / 1024:.2f} TB"
    else:
        return f"{capacity:.2f} GB"

