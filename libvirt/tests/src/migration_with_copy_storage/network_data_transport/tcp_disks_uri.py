from provider.migration import base_steps


def run(test, params, env):
    """
    To verify that the ip and port for copying storage can be specified by
    --disks-uri, --disks-uri will override --listen-address and --migrateuri.

    :param test: test object
    :param params: Dictionary with the test parameters
    :param env: Dictionary with test environment.
    """
    def setup_test():
        migrateuri_and_listen_addr = params.get("migrateuri_and_listen_addr")
        extra = params.get("virsh_migrate_extra")
        if migrateuri_and_listen_addr:
            extra = "%s %s" % (extra, migrateuri_and_listen_addr)
            params.update({"virsh_migrate_extra": extra})

        migration_obj.setup_connection()

    vm_name = params.get("migrate_main_vm")

    vm = env.get_vm(vm_name)
    migration_obj = base_steps.MigrationBase(test, vm, params)

    try:
        setup_test()
        base_steps.prepare_disks_remote(params, vm)
        migration_obj.run_migration()
        migration_obj.verify_default()
    finally:
        migration_obj.cleanup_connection()
        base_steps.cleanup_disks_remote(params, vm)
