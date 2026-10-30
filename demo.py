from accounts import AccountStore

store = AccountStore()
try:
    store.register('learner', 'DemoPassphrase-2026')
    print('Correct password accepted:', store.authenticate('learner', 'DemoPassphrase-2026'))
    print('Wrong password rejected:', not store.authenticate('learner', 'WrongPassphrase-2026'))
    print('SQL injection attempt rejected:', not store.authenticate("' OR 1=1 --", 'DemoPassphrase-2026'))
    print('Demo complete. Only fictional, temporary account data was used.')
finally:
    store.close()
