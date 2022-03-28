import vultr as vr
import digitalocean as do

crawler_choice = """Qual crawler deseja executar?
1 - Vultr
2 - Digital Ocean
3 - Sair
Digite o número da opção desejada: """

crawler_execution_text = """\nCrawler executado com sucesso! O que deseja fazer?
print
save_csv
save_json
Digite a opção desejada: """

while True:
    option = int(input(crawler_choice))
    if option == 1:
        answer = input(crawler_execution_text)
        if answer == "print":
            with vr.pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(vr.vultr_df)
        elif answer == "save_csv":
            vr.vultr_df.to_csv('vultr.csv', index=False)
        elif answer == "save_json":
            vr.vultr_df.to_json('vultr.json', orient="table")
        else:
            print("Resposta Inválida.")

    elif option == 2:
        answer = input(crawler_execution_text)
        if answer == "print":
            with do.pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(do.do_df)
        elif answer == "save_csv":
            do.do_df.to_csv('digital_ocean.csv', index=False)
        elif answer == "save_json":
            do.do_df.to_json('digital_ocean.json', orient="table")
        else:
            print("Resposta Inválida.")
    elif option == 3:
        break
    else:
        print('Resposta inválida.')
