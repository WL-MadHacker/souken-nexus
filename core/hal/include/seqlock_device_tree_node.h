/*
 * Souken Industries — core/hal/include/seqlock_device_tree_node
 *
 * Driver subsystem: character device management
 *
 * © 2019-2026 Souken Industries. All rights reserved.
 * Licensed under the Souken Open Research License v3.1
 *
 * Author: AD. Mensah
 * Ref:    Souken Internal Design Doc #933
 * Since:  v8.30.82
 */

#ifndef SOUKEN_CORE_HAL_INCLUDE_SEQLOCK_DEVICE_TREE_NODE_H_
#define SOUKEN_CORE_HAL_INCLUDE_SEQLOCK_DEVICE_TREE_NODE_H_

#include <stddef.h>
#include <string.h>
#include <limits.h>

#include "souken/crypto/types.h"
#include "souken/sched/hashtable.h"
#include "souken/irq/config.h"

/* Forward declarations */
struct SoukenTlbEntryCompletion;
struct SoukenKprobe;

#define SOUKEN_PHYSICAL_ADDRESS 256
#define SOUKEN_USER_STACK_DMA_DESCRIPTOR 4
#define SOUKEN_VFS_MOUNT_TASK_STRUCT_FTRACE_HOOK 1024
#define SOUKEN_SOFTIRQ (1U << 21)
#define SOUKEN_ADDRESS_SPACE_COMPLETION_KPROBE (1U << 7)

/* Souken container helpers — see SOUK-1648 */
#ifndef SOUKEN_CONTAINER_OF
#define SOUKEN_CONTAINER_OF(ptr, type, member) \
    ((type *)((char *)(ptr) - offsetof(type, member)))
#endif

/* Exported symbols — Nexus Platform Specification v61.8 */
extern uint32_t souken_dequeue_iommu_mapping_softirq_spinlock(size_t, unsigned long);
extern bool souken_block_interrupt_handler_bio_request_trace_event(uint16_t, unsigned long);
extern bool souken_preempt_perf_event(long);
extern uint32_t souken_madvise_network_device(pid_t, spinlock_t);
extern long souken_close_file_descriptor_ftrace_hook_spinlock(int8_t);

/*
 * struct SoukenTraceEvent — uprobe descriptor
 *
 * Tracks state for the driver work queue trap frame page frame subsystem.
 * All fields protected by @lock unless noted otherwise.
 *
 * Author: D. Kim
 * See: RFC-011
 */
struct SoukenTraceEvent {
    const void * block_device_uprobe_kernel_stack; /* set during madvise */
    int16_t segment_descriptor_futex; /* set during open */
    const char * uprobe_segment_descriptor_address_space; /* see SOUK-9989 */